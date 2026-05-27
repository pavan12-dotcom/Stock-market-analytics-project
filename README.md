<div align="center">

# 📈 Real-Time Stock Market Analytics Platform

### An end-to-end data analytics platform for 10 major US equities with live data, interactive dashboard, portfolio optimization & Excel reporting.

[![Live Dashboard](https://img.shields.io/badge/🚀%20Live%20Dashboard-Visit%20Now-blueviolet?style=for-the-badge)](https://pavan12-dotcom.github.io/Stock-market-analytics-project/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/pavan12-dotcom/Stock-market-analytics-project)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance%20API-6001D2?style=flat)
![Chart.js](https://img.shields.io/badge/Dashboard-Chart.js%204.4-FF6384?style=flat)
![GitHub Pages](https://img.shields.io/badge/Deployed-GitHub%20Pages-222222?style=flat&logo=github)
![Excel](https://img.shields.io/badge/Report-Excel%205--Tab-217346?style=flat&logo=microsoft-excel)
![Status](https://img.shields.io/badge/Status-Production%20Ready-00d084?style=flat)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dashboard Tabs](#-dashboard-tabs)
- [Analytics Metrics](#-analytics-metrics)
- [Charts](#-charts)
- [Quick Start](#-quick-start)
- [Data Pipeline](#-data-pipeline)
- [Portfolio Optimization](#-portfolio-optimization)
- [Deployment](#-deployment)
- [Configuration](#-configuration)

---

## 🎯 Overview

This platform solves a real-world data analyst challenge: **no single tool combines live stock prices, risk metrics, portfolio optimization, and visual reporting in one place**.

> Built for Data Analyst portfolios — demonstrating Python EDA, financial statistics, interactive visualization, and cloud deployment.

**Tracks 10 major US equities:**

| Ticker | Company | Sector |
|--------|---------|--------|
| AAPL | Apple Inc. | Technology |
| MSFT | Microsoft Corporation | Technology |
| GOOGL | Alphabet Inc. | Communication Services |
| AMZN | Amazon.com Inc. | Consumer Cyclical |
| TSLA | Tesla Inc. | Consumer Cyclical |
| NVDA | NVIDIA Corporation | Technology |
| JPM | JPMorgan Chase & Co. | Financial Services |
| JNJ | Johnson & Johnson | Healthcare |
| V | Visa Inc. | Financial Services |
| WMT | Walmart Inc. | Consumer Defensive |

**+ SPY** (S&P 500 ETF) as benchmark

---

## 🚀 Live Demo

> **[https://pavan12-dotcom.github.io/Stock-market-analytics-project/](https://pavan12-dotcom.github.io/Stock-market-analytics-project/)**

- ✅ Hosted entirely on GitHub Pages, auto-updates on every repository push
- ✅ Real data from Yahoo Finance — last 1 year of trading history
- ✅ No login required — open and explore immediately

---

## ✨ Features

### 📊 Interactive Dashboard (HTML + Chart.js)
- **4 Tab System** — Overview, Risk Analytics, Portfolio, Monte Carlo
- **KPI Strip** — Live price, daily change, annualised return, volatility, Sharpe, Max Drawdown
- **Price Chart** — Candlestick-style with MA50/MA200 overlays + SPY benchmark
- **Timeframe Selector** — 1M / 3M / 6M / 1Y view
- **Insight Ticker** — Auto-scrolling AI-style market insights

### 📉 Risk Analytics
- Drawdown timeline chart
- Rolling 30-Day Volatility
- VaR 95% vs CVaR 95% comparison bar chart
- Risk metrics heatmap across all stocks

### 💼 Portfolio Optimization
- **Max Sharpe Ratio** portfolio (Monte Carlo simulation — 5,000 portfolios)
- **Min Variance** portfolio
- **Equal Weight** benchmark
- **Custom Portfolio Builder** — drag sliders to set your own allocation in real-time
- Strategy comparison bar chart

### 🎲 Monte Carlo Simulation
- 200 simulation paths × 30 future trading days
- P10 / P50 / P90 forecast bands
- Per-stock forecast with current price as anchor

### 📈 Python Analysis (6 Charts)
1. Normalised Performance (100-indexed)
2. Monthly Returns Heatmap
3. Risk vs Return Scatter
4. Correlation Matrix Heatmap
5. Price + Volume Timeline
6. Rolling 30-Day Sharpe Ratio

### 📑 Excel Report (5-Tab Workbook)
| Tab | Content |
|-----|---------|
| Summary | Price, returns, risk metrics for all 10 stocks |
| Monthly Returns | Pivot heatmap by month |
| Risk Analysis | Sharpe, Sortino, Calmar, VaR, CVaR, Max Drawdown |
| Correlation | Full 10×10 correlation matrix |
| Raw Data | Cleaned daily OHLCV data |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Data Source** | Yahoo Finance API via `yfinance` |
| **Analysis** | Python — `pandas`, `numpy`, `scipy` |
| **Visualization (Python)** | `matplotlib`, `seaborn` |
| **Dashboard** | Vanilla HTML5 + CSS3 + Chart.js 4.4 |
| **Fonts** | IBM Plex Mono, IBM Plex Sans (Google Fonts) |
| **Deployment** | GitHub Pages (auto-deploy from GitHub repository) |
| **Excel Report** | `openpyxl` with conditional formatting |
| **Scheduling** | Python `schedule` library |

---

## 📁 Project Structure

```
Stock-market-analytics-project/
│
├── 📊 Stock_Live_Dashboard.html     # Main interactive dashboard (4 tabs, 8+ charts)
│
├── 🐍 generate_dashboard_data.py    # Core pipeline: fetch → calculate → export live_data.js
├── 🐍 stock_analysis.py             # Python EDA: 6 matplotlib/seaborn charts + stats
├── 🐍 build_excel.py                # Generates 5-tab formatted Excel workbook
├── 🐍 fetch_live_data.py            # Alpha Vantage API integration (optional)
├── 🐍 daily_scheduler.py            # Auto-runs data pipeline on a schedule
│
├── 📂 data/
│   ├── live_data.js                 # Auto-generated: real stock data as JS object
│   ├── stock_history.csv            # Historical price data (CSV)
│   ├── latest_snapshot.csv          # Most recent prices snapshot
│   ├── stock_stats.csv              # Computed metrics (Sharpe, VaR, etc.)
│   └── generate_stock_data.py       # Data utility script
│
├── 📂 charts/
│   ├── chart1_normalised_performance.png
│   ├── chart2_monthly_heatmap.png
│   ├── chart3_risk_return.png
│   ├── chart4_correlation.png
│   ├── chart5_price_volume.png
│   └── chart6_rolling_sharpe.png
│
├── 📄 Stock_Market_Analytics.xlsx   # Pre-generated 5-tab Excel report
├── 📄 netlify.toml                  # Netlify deployment config + cache headers
├── 📄 .env.example                  # Template for API keys
└── 📄 .gitignore                    # Python, Node, env exclusions
```

---

## 📱 Dashboard Tabs

### Tab 1 — Overview
The main view showing price chart with MA50/MA200 overlays and SPY benchmark, plus a Risk vs Return scatter plot. Below that: returns distribution histogram, correlation matrix, and rolling Sharpe chart.

### Tab 2 — Risk Analytics
Four charts: Drawdown Timeline, Rolling 30-Day Volatility, VaR vs CVaR bar chart, and a Risk Metrics Heatmap comparing all stocks side-by-side.

### Tab 3 — Portfolio
Three strategies compared: Equal Weight, Max Sharpe, Min Variance. Includes an allocation pie chart, strategy comparison bar chart, and a **Custom Portfolio Builder** with real-time sliders.

### Tab 4 — Monte Carlo
200-path, 30-day forward simulation using Geometric Brownian Motion. Shows P10/P50/P90 forecast cones per stock.

---

## 📐 Analytics Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| **Annualised Return** | `mean(daily_ret) × 252` | Expected yearly return |
| **Annualised Volatility** | `std(daily_ret) × √252` | Risk measure |
| **Sharpe Ratio** | `(Ann_Ret − RF) / Ann_Vol` | Risk-adjusted return (RF = 5.25%) |
| **Sortino Ratio** | `Sharpe × 0.8` | Downside-only risk adjustment |
| **Calmar Ratio** | `Ann_Ret / Max_Drawdown` | Return per unit of drawdown |
| **Max Drawdown** | `min(price/peak − 1)` | Worst peak-to-trough loss |
| **VaR 95%** | 5th percentile of daily returns | Daily loss at 95% confidence |
| **CVaR 95%** | Mean of returns below VaR | Expected loss beyond VaR |
| **MA Crossover** | MA50 crosses MA200 | Golden Cross / Death Cross signal |
| **Monte Carlo** | `GBM: dS = S(μdt + σdW)` | 200 paths, 30-day forecast |

---

## 📈 Charts

<div align="center">

| Chart | Preview |
|-------|---------|
| Normalised Performance | `charts/chart1_normalised_performance.png` |
| Monthly Heatmap | `charts/chart2_monthly_heatmap.png` |
| Risk vs Return | `charts/chart3_risk_return.png` |
| Correlation Matrix | `charts/chart4_correlation.png` |
| Price + Volume | `charts/chart5_price_volume.png` |
| Rolling Sharpe | `charts/chart6_rolling_sharpe.png` |

</div>

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/pavan12-dotcom/Stock-market-analytics-project.git
cd Stock-market-analytics-project
```

### 2. Install Dependencies
```bash
pip install yfinance pandas numpy matplotlib seaborn openpyxl python-dotenv requests
```

### 3. Generate Fresh Data
```bash
python generate_dashboard_data.py
```
> This fetches the last 1 year of data from Yahoo Finance and writes `data/live_data.js`

### 4. Open the Dashboard
```bash
# Open directly in browser (Windows)
start Stock_Live_Dashboard.html

# Or use a local server for best results
python -m http.server 8080
# Then visit: http://localhost:8080
```

### 5. Run Full Analysis (Python Charts + Excel)
```bash
python stock_analysis.py        # Generates 6 charts in /charts/
python build_excel.py           # Generates 5-tab Excel workbook
```

### 6. Auto-refresh Data Daily (Optional)
```bash
python daily_scheduler.py       # Runs generate_dashboard_data.py every 24h
```

---

## 🔄 Data Pipeline

```
Yahoo Finance API
      │
      ▼
generate_dashboard_data.py
      │
      ├── fetch_data_via_yahoo()     → 1 year OHLCV for all 10 stocks + SPY
      ├── calculate_metrics()        → Ann Return, Volatility, Sharpe per stock
      ├── generate_enriched()        → MA50, MA200, Roll_Vol, Monte Carlo
      ├── portfolio_optimization()   → 5,000 random portfolios → Max Sharpe + Min Var
      └── generate_live_data_js()    → Writes data/live_data.js
                  │
                  ▼
      Stock_Live_Dashboard.html
      (loads live_data.js → renders all charts)
```

**Data flows:**
- `data/live_data.js` — Primary source for the HTML dashboard
- `data/stock_history.csv` — Full price history for Python scripts
- `data/latest_snapshot.csv` — Current prices for quick reference
- `charts/*.png` — Static output from `stock_analysis.py`

---

## 💼 Portfolio Optimization

Uses **Monte Carlo Portfolio Simulation** with 5,000 random weight combinations:

```python
for i in range(5000):
    weights = random_weights(n_stocks)        # Random, sum to 1
    p_return = weights @ mean_returns          # Expected return
    p_vol    = sqrt(weights.T @ cov @ weights) # Portfolio volatility
    p_sharpe = (p_return - RF_RATE) / p_vol   # Sharpe ratio

max_sharpe_portfolio = argmax(sharpe_ratios)
min_variance_portfolio = argmin(volatilities)
```

**Result:** Efficient Frontier portfolios with exact per-stock weights displayed in the dashboard.

---

## 🚀 Deployment

The dashboard is deployed completely free using **GitHub Pages** directly from the repository code. 

```
git push origin main
    │
    ▼ (Trigger GitHub Pages Action)
GitHub Pages CDN
    │
    ├── Serves index.html (immediate redirect)
    ├── Serves Stock_Live_Dashboard.html (main dashboard UI)
    └── Serves data/live_data.js (holds latest live stock data)
```

### How to Enable GitHub Pages (One-time Setup)
1. Go to your GitHub repository: [pavan12-dotcom/Stock-market-analytics-project](https://github.com/pavan12-dotcom/Stock-market-analytics-project)
2. Click **Settings** ⚙️ on the top menu.
3. On the left sidebar, click **Pages** under the "Code and automation" section.
4. Under **Build and deployment**:
   - **Source**: Select `Deploy from a branch`.
   - **Branch**: Select `main` and folder `/ (root)`.
5. Click **Save** 💾.
6. Within 1-2 minutes, your dashboard will be live at: **`https://pavan12-dotcom.github.io/Stock-market-analytics-project/`**

---

## ⚙️ Configuration

### Environment Variables (`.env`)
Copy `.env.example` and fill in:

```env
# Optional: Alpha Vantage for real-time intraday data
ALPHA_VANTAGE_API_KEY=your_key_here

# Yahoo Finance is used by default (no key needed)
DATA_PROVIDER=yahoo
```

### Customize Tickers
In `generate_dashboard_data.py`:
```python
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
           'NVDA', 'JPM', 'JNJ', 'V', 'WMT']
```

### Risk-Free Rate
```python
RF_RATE = 0.0525  # 5.25% US T-bill (update as needed)
```

---

## 🗂 Key Files Reference

| File | Purpose | Run |
|------|---------|-----|
| `generate_dashboard_data.py` | **Main pipeline** — fetches data, computes all metrics, outputs `live_data.js` | `python generate_dashboard_data.py` |
| `Stock_Live_Dashboard.html` | **Interactive dashboard** — 4 tabs, 8+ charts, portfolio builder | Open in browser |
| `stock_analysis.py` | **EDA script** — 6 Python charts saved as PNG | `python stock_analysis.py` |
| `build_excel.py` | **Excel report** — 5-tab formatted workbook | `python build_excel.py` |
| `fetch_live_data.py` | Alpha Vantage real-time integration | `python fetch_live_data.py` |
| `daily_scheduler.py` | Auto-scheduler for daily data refresh | `python daily_scheduler.py` |

---

<div align="center">

**Built with ❤️ for Data Analytics portfolios**

[![Live Demo](https://img.shields.io/badge/🚀%20View%20Live%20Dashboard-pavan12--dotcom.github.io-blueviolet?style=for-the-badge)](https://pavan12-dotcom.github.io/Stock-market-analytics-project/)

*Python · Yahoo Finance · Chart.js · GitHub Pages · Excel*

</div>
