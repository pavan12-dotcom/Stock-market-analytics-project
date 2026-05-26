"""
=============================================================
LIVE DATA FETCHER — Run this on YOUR machine
=============================================================
Install dependencies first:
    pip install yfinance pandas openpyxl matplotlib seaborn

Then run:
    python3 fetch_live_data.py

This will:
  1. Pull real-time stock data from Yahoo Finance
  2. Save to data/stock_history.csv  (replaces simulated data)
  3. Regenerate all charts with live data
  4. Rebuild the Excel report with live prices
=============================================================
"""

import subprocess, sys, os

# Auto-install yfinance if missing
try:
    import yfinance as yf
except ImportError:
    print("Installing yfinance...")
    subprocess.check_call([sys.executable,'-m','pip','install','yfinance'])
    import yfinance as yf

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

TICKERS  = ['AAPL','MSFT','GOOGL','AMZN','TSLA','NVDA','JPM','JNJ','V','WMT']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR,'charts'), exist_ok=True)

print("="*55)
print("📡 FETCHING LIVE DATA FROM YAHOO FINANCE")
print("="*55)

end   = datetime.today()
start = end - timedelta(days=400)

print(f"\nDownloading {len(TICKERS)} stocks: {', '.join(TICKERS)}")
raw = yf.download(TICKERS, start=start, end=end, auto_adjust=True)
close  = raw['Close']
high   = raw['High']
low    = raw['Low']
open_  = raw['Open']
volume = raw['Volume']

# Build long-format dataframe
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
df = df.sort_values(['ticker','date']).reset_index(drop=True)
df['daily_ret'] = df.groupby('ticker')['close'].pct_change()

df.to_csv(f'{DATA_DIR}/stock_history.csv', index=False)
print(f"\n✓ Saved {len(df):,} rows to data/stock_history.csv")

# Latest snapshot
latest = df.groupby('ticker').last().reset_index()
latest['change_pct'] = latest['daily_ret'] * 100
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

print("\n" + "="*55)
print("✓ Live data ready! Now run:")
print("   python3 stock_analysis.py       → regenerate charts")
print("   python3 build_excel.py          → rebuild Excel report")
print("="*55)
