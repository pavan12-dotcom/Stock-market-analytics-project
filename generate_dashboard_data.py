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
        stock_data[row['ticker']] = {
            'name': row['name'],
            'sector': row['sector'],
            'price': round(row['close'], 2),
            'chg': round(row['change_pct'], 2),
            'ret': round(row['ann_return_pct'], 2),
            'vol': round(row['ann_vol'], 2),
            'sharpe': round(row['sharpe'], 2)
        }
    
    # History data for each ticker
    histories = {}
    for ticker in TICKERS:
        ticker_data = df_history[df_history['ticker'] == ticker].sort_values('date')
        histories[ticker] = [round(float(p), 2) for p in ticker_data['close'].values]
    
    # Build the JavaScript object
    live_data = {
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'stockData': stock_data,
        'dateLabels': date_labels,
        'histories': histories
    }
    
    # Generate JavaScript file
    js_content = f"""window.LIVE_DATA = {json.dumps(live_data, indent=2)};
"""
    
    with open(output_path, 'w') as f:
        f.write(js_content)
    
    print(f"✓ Generated {output_path}")

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
