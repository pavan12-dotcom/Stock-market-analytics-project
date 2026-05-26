import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

STOCKS = {
    'AAPL':  {'name': 'Apple Inc.',          'sector': 'Technology',    'price': 189.50, 'beta': 1.2},
    'MSFT':  {'name': 'Microsoft Corp.',     'sector': 'Technology',    'price': 415.20, 'beta': 0.9},
    'GOOGL': {'name': 'Alphabet Inc.',       'sector': 'Technology',    'price': 175.80, 'beta': 1.1},
    'AMZN':  {'name': 'Amazon.com Inc.',     'sector': 'Consumer',      'price': 198.40, 'beta': 1.3},
    'TSLA':  {'name': 'Tesla Inc.',          'sector': 'Automotive',    'price': 248.50, 'beta': 2.0},
    'NVDA':  {'name': 'NVIDIA Corp.',        'sector': 'Technology',    'price': 875.40, 'beta': 1.8},
    'JPM':   {'name': 'JPMorgan Chase',      'sector': 'Finance',       'price': 198.20, 'beta': 1.1},
    'JNJ':   {'name': 'Johnson & Johnson',   'sector': 'Healthcare',    'price': 152.30, 'beta': 0.6},
    'V':     {'name': 'Visa Inc.',           'sector': 'Finance',       'price': 278.90, 'beta': 0.9},
    'WMT':   {'name': 'Walmart Inc.',        'sector': 'Retail',        'price': 68.40,  'beta': 0.5},
}

end_date = datetime(2025, 3, 1)
start_date = end_date - timedelta(days=365)
trading_days = pd.bdate_range(start_date, end_date)

all_data = []
for ticker, info in STOCKS.items():
    price = info['price'] * 0.85  # start lower for growth
    beta = info['beta']
    prices = []
    for day in trading_days:
        daily_return = np.random.normal(0.0004, 0.015 * beta)
        # Add slight uptrend for tech stocks
        if info['sector'] == 'Technology':
            daily_return += 0.0003
        price = price * (1 + daily_return)
        volume = int(np.random.normal(45_000_000, 10_000_000) * (1 + abs(daily_return) * 10))
        high   = price * (1 + abs(np.random.normal(0, 0.005)))
        low    = price * (1 - abs(np.random.normal(0, 0.005)))
        open_  = price * (1 + np.random.normal(0, 0.003))
        prices.append({
            'ticker': ticker, 'name': info['name'], 'sector': info['sector'],
            'date': day.date(), 'open': round(open_, 2), 'high': round(high, 2),
            'low': round(low, 2), 'close': round(price, 2), 'volume': max(volume, 1_000_000),
            'beta': beta
        })
    all_data.extend(prices)

df = pd.DataFrame(all_data)
df['date'] = pd.to_datetime(df['date'])
df.to_csv('/home/claude/stock_project/data/stock_history.csv', index=False)

# Latest snapshot
latest = df.groupby('ticker').last().reset_index()
prev = df.groupby('ticker').apply(lambda x: x.iloc[-2]).reset_index(drop=True)[['ticker','close']].rename(columns={'close':'prev_close'})
latest = latest.merge(prev, on='ticker')
latest['change']    = latest['close'] - latest['prev_close']
latest['change_pct'] = (latest['change'] / latest['prev_close'] * 100).round(2)
latest['52w_high']  = df.groupby('ticker')['high'].max().values
latest['52w_low']   = df.groupby('ticker')['low'].min().values
latest['avg_vol']   = df.groupby('ticker')['volume'].mean().round(0).astype(int).values
latest['market_cap'] = (latest['close'] * np.random.randint(5_000_000_000, 50_000_000_000, len(latest))).round(-6)
latest.to_csv('/home/claude/stock_project/data/latest_snapshot.csv', index=False)

print(f"Generated {len(df):,} rows across {len(STOCKS)} stocks over {len(trading_days)} trading days")
print(latest[['ticker','name','close','change_pct','volume']].to_string(index=False))
