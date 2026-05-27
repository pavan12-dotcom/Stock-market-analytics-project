"""
=============================================================
LIVE DATA FETCHER — Supports Alpha Vantage & Yahoo Finance
=============================================================
Install dependencies first:
    pip install requests pandas openpyxl matplotlib seaborn yfinance

Setup Alpha Vantage API (optional but recommended):
  1. Get FREE API key at: https://www.alphavantage.co/
  2. Set environment variable: export ALPHA_VANTAGE_API_KEY="your_api_key"
  3. Or create .env file with: ALPHA_VANTAGE_API_KEY=your_api_key

Usage:
  python3 fetch_live_data.py                    # Auto-detect (Alpha Vantage or Yahoo)
  python3 fetch_live_data.py --provider yahoo   # Force Yahoo Finance
  python3 fetch_live_data.py --provider alpha   # Force Alpha Vantage
=============================================================
"""

import subprocess, sys, os, json, time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Auto-install requests if missing
try:
    import requests
except ImportError:
    print("Installing requests...")
    subprocess.check_call([sys.executable,'-m','pip','install','requests'])
    import requests

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

TICKERS  = ['AAPL','MSFT','GOOGL','AMZN','TSLA','NVDA','JPM','JNJ','V','WMT']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR,'charts'), exist_ok=True)

# ─── ALPHA VANTAGE DATA FETCHER ───────────────────────────────────
class AlphaVantageAPI:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', '')
        self.base_url = 'https://www.alphavantage.co/query'
        self.call_count = 0
        
    def fetch_daily(self, ticker, outputsize='full'):
        """Fetch daily prices (5 calls per minute limit on free tier)
        
        Args:
            ticker: Stock symbol (e.g., 'AAPL')
            outputsize: 'compact' (100 days) or 'full' (20+ years, ~1260 trading days per year)
        """
        if not self.api_key:
            raise ValueError("Alpha Vantage API key not found. Set ALPHA_VANTAGE_API_KEY env var.")
        
        # Rate limiting (5 calls per minute = 12 seconds per call)
        if self.call_count > 0:
            time.sleep(12)
        
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'outputsize': outputsize,  # 'full' = ~20+ years of data
            'apikey': self.api_key
        }
        
        try:
            print(f"  📥 Fetching {ticker}...", end='', flush=True)
            resp = requests.get(self.base_url, params=params, timeout=15)
            resp.raise_for_status()
            self.call_count += 1
            
            data = resp.json()
            
            if 'Error Message' in data:
                raise Exception(f"API Error: {data['Error Message']}")
            if 'Note' in data:
                raise Exception(f"Rate limit: {data['Note']}")
            if 'Time Series (Daily)' not in data:
                keys = list(data.keys()) if isinstance(data, dict) else []
                raise Exception(f"No time series (keys: {keys})")
            
            ts = data['Time Series (Daily)']
            if not ts:
                raise Exception("Empty time series")
            
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
            
            if not rows:
                raise Exception("No valid OHLCV data")
            
            print(f" ✓ ({len(rows)} days)")
            return pd.DataFrame(rows)
        
        except Exception as e:
            print(f" ✗ ({str(e)[:50]})")
            return None
    
    def fetch_quote(self, ticker):
        """Fetch latest quote & company info"""
        if not self.api_key:
            return {}
        
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': ticker,
                'apikey': self.api_key
            }
            resp = requests.get(self.base_url, params=params, timeout=5)
            data = resp.json()
            
            if 'Global Quote' in data:
                gq = data['Global Quote']
                return {
                    'close': float(gq.get('05. price', 0)),
                    'change_pct': float(gq.get('10. change percent', '0').rstrip('%'))
                }
        except:
            pass
        return {}

# ─── YAHOO FINANCE FALLBACK ───────────────────────────────────────
def fetch_yahoo_finance():
    """Fallback to Yahoo Finance"""
    try:
        import yfinance as yf
    except ImportError:
        print("Installing yfinance...")
        subprocess.check_call([sys.executable,'-m','pip','install','yfinance'])
        import yfinance as yf
    
    end   = datetime.today()
    start = end - timedelta(days=400)
    
    print(f"Downloading {len(TICKERS)} stocks...")
    raw = yf.download(TICKERS, start=start, end=end, auto_adjust=True, progress=True)
    
    close  = raw['Close']
    high   = raw['High']
    low    = raw['Low']
    open_  = raw['Open']
    volume = raw['Volume']
    
    rows = []
    for ticker in TICKERS:
        try:
            info = yf.Ticker(ticker).info
            name   = info.get('longName', ticker)
            sector = info.get('sector', 'N/A')
            beta   = info.get('beta', 1.0) or 1.0
        except:
            name, sector, beta = ticker, 'N/A', 1.0
        
        for dt in close.index:
            rows.append({
                'ticker':   ticker,
                'name':     name,
                'sector':   sector,
                'beta':     beta,
                'date':     dt.date(),
                'open':     round(float(open_[ticker][dt]),  2) if ticker in open_.columns  else None,
                'high':     round(float(high[ticker][dt]),   2) if ticker in high.columns   else None,
                'low':      round(float(low[ticker][dt]),    2) if ticker in low.columns    else None,
                'close':    round(float(close[ticker][dt]),  2) if ticker in close.columns  else None,
                'volume':   int(volume[ticker][dt])               if ticker in volume.columns else None,
            })
    
    df = pd.DataFrame(rows).dropna(subset=['close'])
    df['date'] = pd.to_datetime(df['date'])
    return df

# ─── MAIN EXECUTION ───────────────────────────────────────────────
def main():
    provider = 'auto'
    if '--provider' in sys.argv:
        idx = sys.argv.index('--provider')
        provider = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'auto'
    
    print("="*60)
    print("📡 FETCHING LIVE STOCK DATA")
    print("="*60)
    
    df = None
    
    # Try Alpha Vantage first (if provider is auto or alpha)
    if provider in ['auto', 'alpha']:
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if api_key:
            print("\n🔷 Using Alpha Vantage API (FULL DATA - Past 5+ Years)...")
            av = AlphaVantageAPI()
            all_dfs = []
            
            for ticker in TICKERS:
                # Use 'full' to get all available historical data (20+ years)
                ticker_df = av.fetch_daily(ticker, outputsize='full')
                if ticker_df is not None:
                    all_dfs.append(ticker_df)
            
            if all_dfs:
                df = pd.concat(all_dfs, ignore_index=True)
                df['date'] = pd.to_datetime(df['date'])
                
                # Filter to past 1 year from today
                one_year_ago = datetime.now() - timedelta(days=365)
                df = df[df['date'] >= one_year_ago]
                
                print(f"   ✓ Filtered to past 1 year: {df['date'].min().date()} to {df['date'].max().date()}")
                # Add company info from Yahoo as fallback
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
                except:
                    pass
                print(f"\n✓ Alpha Vantage fetch completed ({len(all_dfs)}/{len(TICKERS)} tickers)")
        else:
            if provider == 'alpha':
                print("\n❌ Alpha Vantage API key not found!")
                print("   Set ALPHA_VANTAGE_API_KEY environment variable")
                sys.exit(1)
    
    # Fallback to Yahoo Finance if needed
    if df is None or len(df) == 0:
        print("\n🟨 Using Yahoo Finance (fallback)...")
        try:
            df = fetch_yahoo_finance()
            print("\n✓ Yahoo Finance fetch completed")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)
    
    # Ensure required columns
    for col in ['name', 'sector', 'beta']:
        if col not in df.columns:
            df[col] = df['ticker'] if col == 'name' else ('Technology' if col == 'sector' else 1.0)
    
    # Sort and compute returns
    df = df.sort_values(['ticker','date']).reset_index(drop=True)
    df['daily_ret'] = df.groupby('ticker')['close'].pct_change()
    
    # Save to CSV
    df.to_csv(f'{DATA_DIR}/stock_history.csv', index=False)
    print(f"\n✓ Saved {len(df):,} rows to data/stock_history.csv")
    
    # Latest snapshot
    latest = df.groupby('ticker').last().reset_index()
    latest['change_pct'] = (latest['daily_ret'] * 100).round(2)
    w52 = df.groupby('ticker').agg(w52h=('high','max'), w52l=('low','min'), avg_vol=('volume','mean')).reset_index()
    latest = latest.merge(w52, on='ticker')
    latest.to_csv(f'{DATA_DIR}/latest_snapshot.csv', index=False)
    
    # Stats
    stats = df.groupby('ticker')['daily_ret'].agg(
        ann_return=lambda x: x.mean()*252*100,
        ann_vol=lambda x: x.std()*np.sqrt(252)*100
    ).reset_index()
    stats['sharpe'] = stats['ann_return'] / stats['ann_vol']
    stats = stats.merge(latest[['ticker','close','change_pct','name','sector','beta']], on='ticker')
    stats.rename(columns={'close':'last_price'}, inplace=True)
    stats = stats.round(2)
    stats.to_csv(f'{DATA_DIR}/stock_stats.csv', index=False)
    
    print("\n📊 Live Summary:")
    print(stats[['ticker','last_price','change_pct','ann_return','ann_vol','sharpe']].to_string(index=False))
    
    print("\n" + "="*60)
    print("✓ Live data ready! Now run:")
    print("   python3 stock_analysis.py       → regenerate charts")
    print("   python3 build_excel.py          → rebuild Excel report")
    print("="*60)

if __name__ == '__main__':
    main()
