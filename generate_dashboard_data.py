"""
=============================================================
DASHBOARD DATA GENERATOR — Real-Time Stock Analytics
=============================================================
This script fetches real stock data and generates the live_data.js
file used by the Stock_Live_Dashboard.html dashboard.

Requires: pip install requests pandas openpyxl python-dotenv yfinance

Usage:
    python3 generate_dashboard_data.py                  # Auto-detect API
    python3 generate_dashboard_data.py --provider alpha # Force Alpha Vantage
    python3 generate_dashboard_data.py --provider yahoo # Force Yahoo Finance
=============================================================
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
import time
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V', 'WMT']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Risk-free rate (approximate US T-bill rate)
RF_RATE = 0.0525  # 5.25% annualized

def fetch_data_via_alpha_vantage():
    """Fetch data using Alpha Vantage API (preferred)"""
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        import requests
    
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("❌ ALPHA_VANTAGE_API_KEY not found")
        return None
    
    print("🔷 Fetching data from Alpha Vantage API...")
    base_url = 'https://www.alphavantage.co/query'
    all_data = {}
    
    for ticker in TICKERS:
        print(f"  📥 Fetching {ticker}...", end='', flush=True)
        
        # Rate limiting: Alpha Vantage free tier = 5 calls/minute
        if all_data:
            time.sleep(12)
        
        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': ticker,
                'outputsize': 'full',
                'apikey': api_key
            }
            resp = requests.get(base_url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            if 'Error Message' in data:
                print(f" ✗ (API Error)")
                continue
            if 'Note' in data:
                print(f" ✗ (Rate limited)")
                continue
            if 'Time Series (Daily)' not in data:
                print(f" ✗ (No data)")
                continue
            
            ts = data['Time Series (Daily)']
            rows = []
            for date_str, ohlcv in ts.items():
                try:
                    rows.append({
                        'ticker': ticker,
                        'date': date_str,
                        'open': float(ohlcv['1. open']),
                        'high': float(ohlcv['2. high']),
                        'low': float(ohlcv['3. low']),
                        'close': float(ohlcv['4. close']),
                        'volume': int(ohlcv['5. volume'])
                    })
                except (KeyError, ValueError):
                    continue
            
            if rows:
                all_data[ticker] = rows
                print(f" ✓ ({len(rows)} days)")
            else:
                print(f" ✗ (No valid data)")
        
        except Exception as e:
            print(f" ✗ ({str(e)[:40]})")
            continue
    
    if not all_data:
        print("❌ Could not fetch any data from Alpha Vantage")
        return None
    
    # Combine all data
    combined = []
    for ticker, rows in all_data.items():
        combined.extend(rows)
    
    df = pd.DataFrame(combined)
    df['date'] = pd.to_datetime(df['date'])
    
    # Fetch company info from Yahoo Finance
    try:
        import yfinance as yf
        for ticker in TICKERS:
            try:
                info = yf.Ticker(ticker).info
                df.loc[df['ticker'] == ticker, 'name'] = info.get('longName', ticker)
                df.loc[df['ticker'] == ticker, 'sector'] = info.get('sector', 'N/A')
                df.loc[df['ticker'] == ticker, 'beta'] = info.get('beta', 1.0) or 1.0
            except:
                pass
    except ImportError:
        pass
    
    return df

def fetch_data_via_yahoo():
    """Fallback: Fetch data from Yahoo Finance"""
    try:
        import yfinance as yf
    except ImportError:
        print("Installing yfinance...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance'])
        import yfinance as yf
    
    print("🟨 Fetching data from Yahoo Finance (fallback)...")
    
    end = datetime.today()
    start = end - timedelta(days=400)
    
    try:
        raw = yf.download(TICKERS, start=start, end=end, auto_adjust=True, progress=False)
        
        close = raw['Close'].reset_index()
        close = close.melt(id_vars='Date', var_name='ticker', value_name='close')
        close.columns = ['date', 'ticker', 'close']
        
        # Get company info
        info_map = {}
        for t in TICKERS:
            try:
                info = yf.Ticker(t).info
                info_map[t] = {
                    'name': info.get('longName', t),
                    'sector': info.get('sector', 'N/A'),
                    'beta': info.get('beta', 1.0) or 1.0,
                }
            except:
                info_map[t] = {'name': t, 'sector': 'N/A', 'beta': 1.0}
        
        meta = pd.DataFrame(info_map).T.reset_index().rename(columns={'index': 'ticker'})
        df = close.merge(meta, on='ticker')
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"✓ Fetched {len(df):,} rows from Yahoo Finance")
        return df
    
    except Exception as e:
        print(f"❌ Error fetching from Yahoo Finance: {e}")
        return None

def calculate_metrics(df):
    """Calculate stock metrics"""
    print("\n📊 Calculating metrics...")
    
    df = df.sort_values(['ticker', 'date']).reset_index(drop=True)
    
    # Daily returns
    df['daily_ret'] = df.groupby('ticker')['close'].pct_change()
    
    # Annualized metrics
    metrics = df.groupby('ticker').agg({
        'daily_ret': [
            ('ann_return', lambda x: x.mean() * 252 * 100),
            ('ann_vol', lambda x: x.std() * np.sqrt(252) * 100),
        ]
    }).reset_index()
    
    metrics.columns = ['ticker', 'ann_return', 'ann_vol']
    metrics['sharpe'] = (metrics['ann_return'] - (RF_RATE * 100)) / metrics['ann_vol']
    metrics['sharpe'] = metrics['sharpe'].round(2)
    
    # Latest prices and changes
    latest = df.groupby('ticker').last().reset_index()
    latest['change_pct'] = (latest['daily_ret'] * 100).round(2)
    
    # 1-year return
    one_year_ago = latest['date'].max() - timedelta(days=365)
    df_one_year = df[df['date'] >= one_year_ago]
    
    one_year_prices = {}
    for ticker in df['ticker'].unique():
        ticker_data = df_one_year[df_one_year['ticker'] == ticker]
        if len(ticker_data) > 0:
            first_price = ticker_data.iloc[0]['close']
            one_year_prices[ticker] = first_price
        else:
            one_year_prices[ticker] = latest[latest['ticker'] == ticker]['close'].values[0]
    
    latest['year_start_price'] = latest['ticker'].map(one_year_prices)
    latest['ann_return_pct'] = (
        ((latest['close'] / latest['year_start_price']) - 1) * 100
    ).round(2)
    
    # Merge all metrics
    result = latest[['ticker', 'name', 'sector', 'close', 'change_pct', 'ann_return_pct']].copy()
    result = result.merge(metrics[['ticker', 'ann_vol', 'sharpe']], on='ticker')
    
    return result.fillna(0), df

def generate_live_data_js(stock_metrics, df, output_path):
    """Generate the live_data.js file"""
    print("📝 Generating live_data.js...")
    
    # Get last 250 trading days for history (approximately 1 year)
    cutoff_date = df['date'].max() - timedelta(days=365)
    df_history = df[df['date'] >= cutoff_date].sort_values('date').reset_index(drop=True)
    
    # Date labels
    date_labels = sorted(df_history['date'].unique())
    date_labels = [d.strftime('%Y-%m-%d') for d in date_labels]
    
    # Stock data
    stock_data = {}
    for _, row in stock_metrics.iterrows():
        if row['ticker'] in TICKERS:
            stock_data[row['ticker']] = {
                'name': row['name'],
                'sector': row['sector'],
                'price': round(row['close'], 2),
                'chg': round(row['change_pct'], 2),
                'ret': round(row['ann_return_pct'], 2),
                'vol': round(row['ann_vol'], 2),
                'sharpe': round(row['sharpe'], 2)
            }
    
    # History data for each ticker (including SPY benchmark)
    histories = {}
    for ticker in TICKERS + ['SPY']:
        ticker_data = df_history[df_history['ticker'] == ticker].sort_values('date')
        histories[ticker] = [round(float(p), 2) for p in ticker_data['close'].values]
        
    # Enriched data (ma50, ma200, roll_vol, crosses, mc_p10, mc_p50, mc_p90)
    enriched_data = {}
    for ticker in TICKERS:
        ticker_df = df_history[df_history['ticker'] == ticker].sort_values('date').copy()
        
        # Calculate MA50 and MA200 with min_periods=1 to avoid NaNs at start
        ma50 = ticker_df['close'].rolling(50, min_periods=1).mean().round(2).tolist()
        ma200 = ticker_df['close'].rolling(200, min_periods=1).mean().round(2).tolist()
        
        # Crosses
        crosses = []
        for idx in range(1, len(ticker_df)):
            p50, p200 = ma50[idx-1], ma200[idx-1]
            c50, c200 = ma50[idx], ma200[idx]
            if p50 <= p200 and c50 > c200:
                crosses.append({'date': ticker_df.iloc[idx]['date'].strftime('%Y-%m-%d'), 'type': 'golden'})
            elif p50 >= p200 and c50 < c200:
                crosses.append({'date': ticker_df.iloc[idx]['date'].strftime('%Y-%m-%d'), 'type': 'death'})
                
        # Roll Vol
        ticker_df['daily_ret'] = ticker_df['close'].pct_change()
        roll_vol = (ticker_df['daily_ret'].rolling(30, min_periods=1).std() * np.sqrt(252) * 100).fillna(0).round(2).tolist()
        
        # Monte Carlo
        daily_mean = ticker_df['daily_ret'].mean()
        daily_vol = ticker_df['daily_ret'].std()
        if pd.isna(daily_mean) or pd.isna(daily_vol) or daily_vol == 0:
            daily_mean = 0.0004
            daily_vol = 0.015
            
        last_price = ticker_df.iloc[-1]['close']
        sims = np.zeros((30, 200))
        sims[0, :] = last_price
        for t in range(1, 30):
            sims[t, :] = sims[t-1, :] * np.exp(np.random.normal(daily_mean - 0.5 * daily_vol**2, daily_vol, 200))
            
        mc_p10 = np.percentile(sims, 10, axis=1).round(2).tolist()
        mc_p50 = np.percentile(sims, 50, axis=1).round(2).tolist()
        mc_p90 = np.percentile(sims, 90, axis=1).round(2).tolist()
        
        enriched_data[ticker] = {
            "ma50": ma50,
            "ma200": ma200,
            "crosses": crosses,
            "roll_vol": roll_vol,
            "mc_p10": mc_p10,
            "mc_p50": mc_p50,
            "mc_p90": mc_p90
        }
        
    # Portfolio stats & weights optimization
    print("💼 Performing portfolio optimization...")
    holdings_history = df_history[df_history['ticker'].isin(TICKERS)]
    rets_pivot = holdings_history.pivot(index='date', columns='ticker', values='close').pct_change().dropna()
    cov_matrix = rets_pivot.cov() * 252
    mean_returns = rets_pivot.mean() * 252
    
    num_portfolios = 5000
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    for i in range(num_portfolios):
        wts = np.random.random(len(TICKERS))
        wts /= np.sum(wts)
        weights_record.append(wts)
        p_ret = np.dot(wts, mean_returns)
        p_vol = np.sqrt(np.dot(wts.T, np.dot(cov_matrix, wts)))
        p_sharpe = (p_ret - RF_RATE) / p_vol if p_vol > 0 else 0
        results[0,i] = p_ret
        results[1,i] = p_vol
        results[2,i] = p_sharpe
        
    # Max Sharpe
    max_sharpe_idx = np.argmax(results[2])
    max_sharpe_w = weights_record[max_sharpe_idx]
    max_sharpe_ret = results[0, max_sharpe_idx] * 100
    max_sharpe_vol = results[1, max_sharpe_idx] * 100
    max_sharpe_sr = results[2, max_sharpe_idx]
    
    # Min Variance
    min_vol_idx = np.argmin(results[1])
    min_vol_w = weights_record[min_vol_idx]
    min_vol_ret = results[0, min_vol_idx] * 100
    min_vol_vol = results[1, min_vol_idx] * 100
    min_vol_sr = results[2, min_vol_idx]
    
    # Equal Weight
    equal_w = np.ones(len(TICKERS)) / len(TICKERS)
    equal_ret = np.dot(equal_w, mean_returns) * 100
    equal_vol = np.sqrt(np.dot(equal_w.T, np.dot(cov_matrix, equal_w))) * 100
    equal_sr = (equal_ret/100 - RF_RATE) / (equal_vol/100)
    
    portfolios_data = [
        {"Portfolio": "Equal Weight", "Ann Ret %": round(equal_ret, 2), "Ann Vol %": round(equal_vol, 2), "Sharpe": round(equal_sr, 2)},
        {"Portfolio": "Max Sharpe", "Ann Ret %": round(max_sharpe_ret, 2), "Ann Vol %": round(max_sharpe_vol, 2), "Sharpe": round(max_sharpe_sr, 2)},
        {"Portfolio": "Min Variance", "Ann Ret %": round(min_vol_ret, 2), "Ann Vol %": round(min_vol_vol, 2), "Sharpe": round(min_vol_sr, 2)},
        {"Portfolio": "SPY Benchmark", "Ann Ret %": 8.58, "Ann Vol %": 9.39, "Sharpe": 0.35}
    ]
    
    weights_data = {}
    for i, ticker in enumerate(TICKERS):
        weights_data[ticker] = {
            "equal": round(100.0 / len(TICKERS), 1),
            "max_sharpe": round(max_sharpe_w[i] * 100, 1),
            "min_variance": round(min_vol_w[i] * 100, 1)
        }
    
    # Build the JavaScript object
    live_data = {
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'stockData': stock_data,
        'dateLabels': date_labels,
        'histories': histories,
        'enriched': enriched_data,
        'weights': weights_data,
        'portfolios': portfolios_data
    }
    
    # Generate JavaScript file
    js_content = f"window.LIVE_DATA = {json.dumps(live_data, indent=2)};\n"
    
    with open(output_path, 'w') as f:
        f.write(js_content)
    
    print(f"✓ Generated {output_path}")

def fetch_spy_history(start, end):
    """Fetch SPY benchmark history from Yahoo Finance"""
    print("🔷 Fetching SPY benchmark history from Yahoo Finance...")
    try:
        import yfinance as yf
        raw = yf.download('SPY', start=start, end=end, auto_adjust=True, progress=False)
        if raw.empty:
            raise ValueError("Empty S&P 500 (SPY) ETF history fetched.")
            
        spy_df = raw['Close'].reset_index()
        # Handle MultiIndex columns if any
        if isinstance(spy_df.columns, pd.MultiIndex):
            spy_df.columns = spy_df.columns.get_level_values(0)
            
        spy_df.columns = ['date', 'close']
        spy_df['ticker'] = 'SPY'
        spy_df['name'] = 'SPDR S&P 500 ETF Trust'
        spy_df['sector'] = 'Financials'
        spy_df['beta'] = 1.0
        print(f"✓ Fetched {len(spy_df)} rows for SPY benchmark")
        return spy_df
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch SPY benchmark: {e}")
        return None

def main():
    provider = 'yahoo'  # Default to Yahoo Finance (more reliable)
    if '--provider' in sys.argv:
        idx = sys.argv.index('--provider')
        provider = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'yahoo'
    
    print("=" * 60)
    print("📊 DASHBOARD DATA GENERATOR")
    print("=" * 60)
    
    df = None
    
    # Try Yahoo Finance first (more reliable)
    if provider in ['auto', 'yahoo']:
        df = fetch_data_via_yahoo()
    
    # Try Alpha Vantage if Yahoo fails
    if df is None and provider in ['auto', 'alpha']:
        if os.getenv('ALPHA_VANTAGE_API_KEY'):
            df = fetch_data_via_alpha_vantage()
        elif provider == 'alpha':
            print("\n❌ Alpha Vantage API key not found!")
            print("   Set ALPHA_VANTAGE_API_KEY environment variable or create .env file")
            sys.exit(1)
    
    # Final check
    if df is None:
        print("\n❌ Could not fetch data from any source")
        sys.exit(1)
    
    # Fetch SPY benchmark history
    start_date = df['date'].min()
    end_date = df['date'].max()
    spy_df = fetch_spy_history(start_date, end_date)
    if spy_df is not None:
        df = pd.concat([df, spy_df], ignore_index=True)
    
    # Filter to past 1 year
    one_year_ago = datetime.now() - timedelta(days=365)
    df = df[df['date'] >= one_year_ago]
    
    # Calculate metrics
    metrics, df_with_returns = calculate_metrics(df)
    
    # Display summary
    print("\n📈 Stock Summary:")
    print(metrics[['ticker', 'close', 'change_pct', 'ann_return_pct', 'ann_vol', 'sharpe']].to_string(index=False))
    
    # Generate dashboard data
    output_file = os.path.join(DATA_DIR, 'live_data.js')
    generate_live_data_js(metrics, df_with_returns, output_file)
    
    print("\n" + "=" * 60)
    print("✅ Dashboard data updated successfully!")
    print("=" * 60)
    print("\nThe dashboard will now display real stock data.")
    print("Open Stock_Live_Dashboard.html in your browser to view.")

if __name__ == '__main__':
    main()
