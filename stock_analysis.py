"""
=============================================================
REAL-TIME STOCK MARKET ANALYTICS PLATFORM
=============================================================
Run this on your machine to get LIVE data from Yahoo Finance.
Requires: pip install yfinance pandas matplotlib seaborn openpyxl

Usage:
    python3 stock_analysis.py            # uses live data
    python3 stock_analysis.py --offline  # uses cached CSV data
=============================================================
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

OFFLINE = '--offline' in sys.argv
TICKERS = ['AAPL','MSFT','GOOGL','AMZN','TSLA','NVDA','JPM','JNJ','V','WMT']
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Style ─────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'figure.dpi': 130,
    'axes.facecolor': '#0d1117', 'figure.facecolor': '#050810',
    'axes.edgecolor': '#21262d', 'grid.color': '#21262d',
    'text.color': '#e6edf3', 'axes.labelcolor': '#7d8590',
    'xtick.color': '#7d8590', 'ytick.color': '#7d8590',
    'axes.titlecolor': '#e6edf3', 'axes.titlesize': 12,
    'axes.titleweight': 'bold', 'axes.grid': True, 'grid.alpha': 0.4,
})
COLORS = ['#58a6ff','#3fb950','#f78166','#d2a8ff','#ffa657',
          '#39d353','#79c0ff','#a5d6ff','#ffb3b3','#b3f0c0']

# ── Data Loading ──────────────────────────────────────────────────
def load_live_data():
    try:
        import yfinance as yf
        print("📡 Fetching LIVE data from Yahoo Finance...")
        end   = datetime.today()
        start = end - timedelta(days=365)
        raw   = yf.download(TICKERS, start=start, end=end, auto_adjust=True)
        close = raw['Close'].reset_index()
        close = close.melt(id_vars='Date', var_name='ticker', value_name='close')
        close.columns = ['date','ticker','close']
        info_map = {}
        for t in TICKERS:
            try:
                info = yf.Ticker(t).info
                info_map[t] = {
                    'name':   info.get('longName', t),
                    'sector': info.get('sector', 'N/A'),
                    'beta':   info.get('beta', 1.0),
                    'mktcap': info.get('marketCap', 0),
                    'pe':     info.get('trailingPE', 0),
                    'div':    info.get('dividendYield', 0),
                }
            except:
                info_map[t] = {'name':t,'sector':'N/A','beta':1.0,'mktcap':0,'pe':0,'div':0}
        meta = pd.DataFrame(info_map).T.reset_index().rename(columns={'index':'ticker'})
        df = close.merge(meta, on='ticker')
        df['date'] = pd.to_datetime(df['date'])
        df.to_csv(f'{OUTPUT_DIR}/data/stock_history.csv', index=False)
        print(f"✓ Live data loaded: {len(df):,} rows")
        return df
    except ImportError:
        print("⚠️  yfinance not installed. Install with: pip install yfinance")
        print("   Falling back to cached data...")
        return load_offline_data()

def load_offline_data():
    print("📂 Loading cached stock data...")
    df = pd.read_csv(f'{OUTPUT_DIR}/data/stock_history.csv', parse_dates=['date'])
    print(f"✓ Loaded {len(df):,} rows from cache")
    return df

df = load_offline_data() if OFFLINE else load_live_data()

# Ensure we have all needed columns
if 'name'   not in df.columns: df['name']   = df['ticker']
if 'sector' not in df.columns: df['sector'] = 'Technology'
if 'beta'   not in df.columns: df['beta']   = 1.0

# Sort and compute daily returns
df = df.sort_values(['ticker','date']).reset_index(drop=True)
df['prev_close'] = df.groupby('ticker')['close'].shift(1)
df['daily_ret']  = (df['close'] - df['prev_close']) / df['prev_close']

# Latest snapshot per ticker
latest = df.groupby('ticker').last().reset_index()
latest['change_pct'] = latest['daily_ret'] * 100

print(f"\n{'='*55}")
print("STOCK MARKET ANALYTICS — Summary")
print(f"{'='*55}")
print(f"Tickers tracked : {df['ticker'].nunique()}")
print(f"Date range      : {df['date'].min().date()} → {df['date'].max().date()}")
print(f"Total data rows : {len(df):,}")
print()

# ══════════════════════════════════════════════════════════════════
# CHART 1 — Price Performance (Normalised to 100)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#050810')

pivot = df.pivot(index='date', columns='ticker', values='close').dropna()
norm  = pivot / pivot.iloc[0] * 100

for i, col in enumerate(norm.columns):
    ax.plot(norm.index, norm[col], linewidth=1.8, label=col,
            color=COLORS[i % len(COLORS)], alpha=0.9)

ax.axhline(100, color='#21262d', linewidth=1, linestyle='--')
ax.set_title('Normalised Price Performance (Base = 100)', fontsize=13, fontweight='bold', color='#e6edf3')
ax.set_ylabel('Indexed Price')
ax.legend(ncol=5, fontsize=9, framealpha=0.1, loc='upper left',
          labelcolor='#e6edf3', facecolor='#0d1117')
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b %Y'))
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/charts/chart1_normalised_performance.png', bbox_inches='tight', facecolor='#050810')
plt.close()
print("✓ Chart 1: Normalised performance")

# ══════════════════════════════════════════════════════════════════
# CHART 2 — Returns Heatmap (Monthly)
# ══════════════════════════════════════════════════════════════════
df['year_month'] = df['date'].dt.to_period('M')
monthly_ret = df.groupby(['ticker','year_month']).apply(
    lambda x: (x['close'].iloc[-1] / x['close'].iloc[0] - 1) * 100
).reset_index(name='monthly_ret')
heat = monthly_ret.pivot(index='ticker', columns='year_month', values='monthly_ret')
heat.columns = [str(c) for c in heat.columns]

fig, ax = plt.subplots(figsize=(16, 6))
fig.patch.set_facecolor('#050810')
sns.heatmap(heat.fillna(0), annot=True, fmt='.1f', center=0,
            cmap='RdYlGn', linewidths=0.3, ax=ax,
            cbar_kws={'label': 'Monthly Return %'},
            annot_kws={'size': 7, 'color': '#e6edf3'})
ax.set_title('Monthly Returns Heatmap (%)', fontsize=13, fontweight='bold', color='#e6edf3')
ax.set_xlabel('')
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/charts/chart2_monthly_heatmap.png', bbox_inches='tight', facecolor='#050810')
plt.close()
print("✓ Chart 2: Monthly returns heatmap")

# ══════════════════════════════════════════════════════════════════
# CHART 3 — Volatility vs Return (Risk-Return Scatter)
# ══════════════════════════════════════════════════════════════════
stats = df.groupby('ticker')['daily_ret'].agg(
    ann_return=lambda x: x.mean() * 252 * 100,
    ann_vol=lambda x: x.std() * np.sqrt(252) * 100
).reset_index()
stats = stats.merge(latest[['ticker','name']], on='ticker')
stats['sharpe'] = stats['ann_return'] / stats['ann_vol']

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('#050810')
sc = ax.scatter(stats['ann_vol'], stats['ann_return'],
                s=200, c=stats['sharpe'], cmap='RdYlGn',
                zorder=5, edgecolors='#21262d', linewidths=0.5)
plt.colorbar(sc, ax=ax, label='Sharpe Ratio')
for _, row in stats.iterrows():
    ax.annotate(row['ticker'], (row['ann_vol'], row['ann_return']),
                textcoords='offset points', xytext=(8, 4),
                fontsize=9, color='#e6edf3', fontweight='bold')
ax.axhline(0, color='#f78166', linewidth=0.8, linestyle='--', alpha=0.6)
ax.set_xlabel('Annualised Volatility (%)')
ax.set_ylabel('Annualised Return (%)')
ax.set_title('Risk-Return Analysis (Sharpe Ratio)', fontsize=13, fontweight='bold', color='#e6edf3')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/charts/chart3_risk_return.png', bbox_inches='tight', facecolor='#050810')
plt.close()
print("✓ Chart 3: Risk-return scatter")

# ══════════════════════════════════════════════════════════════════
# CHART 4 — Correlation Matrix
# ══════════════════════════════════════════════════════════════════
ret_pivot = df.pivot(index='date', columns='ticker', values='daily_ret').dropna()
corr = ret_pivot.corr()

fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#050810')
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=0.5, ax=ax, mask=False,
            annot_kws={'size': 9}, vmin=-1, vmax=1,
            cbar_kws={'shrink': 0.8})
ax.set_title('Stock Return Correlation Matrix', fontsize=13, fontweight='bold', color='#e6edf3')
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/charts/chart4_correlation.png', bbox_inches='tight', facecolor='#050810')
plt.close()
print("✓ Chart 4: Correlation matrix")

# ══════════════════════════════════════════════════════════════════
# CHART 5 — Candlestick-style OHLC for top 4 stocks
# ══════════════════════════════════════════════════════════════════
top4 = ['AAPL','MSFT','NVDA','TSLA']
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.patch.set_facecolor('#050810')
fig.suptitle('Price & Volume — Top 4 Stocks (Last 90 Days)', fontsize=13, fontweight='bold', color='#e6edf3')

for ax, ticker in zip(axes.flatten(), top4):
    sub = df[df['ticker']==ticker].tail(90).copy()
    colors_bar = ['#3fb950' if r >= 0 else '#f78166' for r in sub['daily_ret'].fillna(0)]
    ax.plot(sub['date'], sub['close'], color=COLORS[top4.index(ticker)], linewidth=1.8)
    ax2 = ax.twinx()
    ax2.bar(sub['date'], sub.get('volume', 0), color=colors_bar, alpha=0.25, width=0.8)
    ax2.set_ylabel('Volume', fontsize=8, color='#7d8590')
    ax2.tick_params(colors='#7d8590', labelsize=7)
    ax2.set_ylim(0, sub.get('volume', pd.Series([1])).max() * 4 if 'volume' in sub.columns else 1)
    ax.set_title(ticker, fontsize=11, fontweight='bold', color='#e6edf3')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${x:.0f}'))
    ax.tick_params(labelsize=8)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=7)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/charts/chart5_price_volume.png', bbox_inches='tight', facecolor='#050810')
plt.close()
print("✓ Chart 5: Price & volume")

# ══════════════════════════════════════════════════════════════════
# CHART 6 — Rolling Sharpe Ratio (30-day)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('#050810')

for i, ticker in enumerate(TICKERS[:6]):
    sub = df[df['ticker']==ticker].copy()
    sub['roll_sharpe'] = (sub['daily_ret'].rolling(30).mean() /
                          sub['daily_ret'].rolling(30).std()) * np.sqrt(252)
    ax.plot(sub['date'], sub['roll_sharpe'], linewidth=1.5,
            label=ticker, color=COLORS[i], alpha=0.85)

ax.axhline(0, color='#f78166', linewidth=0.8, linestyle='--', alpha=0.6)
ax.axhline(1, color='#3fb950', linewidth=0.8, linestyle='--', alpha=0.4)
ax.set_title('30-Day Rolling Sharpe Ratio', fontsize=13, fontweight='bold', color='#e6edf3')
ax.set_ylabel('Sharpe Ratio')
ax.legend(ncol=6, fontsize=9, framealpha=0.1, loc='upper left',
          labelcolor='#e6edf3', facecolor='#0d1117')
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b %Y'))
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/charts/chart6_rolling_sharpe.png', bbox_inches='tight', facecolor='#050810')
plt.close()
print("✓ Chart 6: Rolling Sharpe ratio")

# ══════════════════════════════════════════════════════════════════
# Save summary stats for Excel
# ══════════════════════════════════════════════════════════════════
stats_out = stats.merge(
    latest[['ticker','close','change_pct']].rename(columns={'close':'last_price'}),
    on='ticker'
).round(2)
stats_out.to_csv(f'{OUTPUT_DIR}/data/stock_stats.csv', index=False)

print(f"\n{'='*55}")
print("ANALYSIS COMPLETE — All charts saved to /charts/")
print(f"{'='*55}")
print("\nRisk-Return Summary:")
print(stats_out[['ticker','last_price','change_pct','ann_return','ann_vol','sharpe']].to_string(index=False))
