# 📈 Real-Time Stock Market Analytics Platform

[![GitHub Repo](https://img.shields.shields.shields.shields.io/badge/GitHub-Repository-blue?style=flat&logo=github&logoColor=white)](https://github.com/pavan12-dotcom/Stock-market-analytics-project)
[![GitHub Stars](https://img.shields.shields.shields.shields.io/github/stars/pavan12-dotcom/Stock-market-analytics-project?style=flat)](https://github.com/pavan12-dotcom/Stock-market-analytics-project/stargazers)
[![GitHub Forks](https://img.shields.shields.shields.shields.io/github/forks/pavan12-dotcom/Stock-market-analytics-project?style=flat)](https://github.com/pavan12-dotcom/Stock-market-analytics-project/network/members)
![Python](https://img.shields.shields.shields.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Yahoo Finance](https://img.shields.shields.shields.shields.io/badge/Data-Yahoo%20Finance%20API-6001D2?style=flat)
![Excel](https://img.shields.shields.shields.shields.io/badge/Report-Excel%205--Tab-217346?style=flat&logo=microsoft-excel&logoColor=white)
![Chart.js](https://img.shields.shields.shields.shields.io/badge/Dashboard-Chart.js-FF6384?style=flat)
![Status](https://img.shields.shields.shields.shields.io/badge/Status-Production%20Ready-00d084?style=flat)

An end-to-end Data Analyst project that tracks **10 major stocks** (AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, JPM, JNJ, V, WMT) with live data from Yahoo Finance — delivering a Python analysis pipeline, interactive HTML dashboard, and a professional Excel report.

---

[![Live Dashboard](https://img.shields.shields.shields.shields.io/badge/Live-Dashboard-blueviolet?style=flat&logo=netlify&logoColor=white)](https://stock-analysis-dashboards.netlify.app)
[![GitHub Repo](https://img.shields.shields.shields.shields.io/badge/View_on-GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/pavan12-dotcom/Stock-market-analytics-project)

## 📋 Problem Statement

### Background
Individual investors and financial analysts face a significant challenge in today's fast-moving stock market — **data is scattered, hard to interpret, and rarely presented in a way that drives actionable decisions**. Most people can see a stock price, but very few can quickly answer:

- *Which stock gives the best return for the risk taken?*
- *Are my stocks moving together (poor diversification) or independently?*
- *Which months historically perform best for each stock?*
- *Is a stock's recent performance driven by momentum or just noise?*

### Problem
> **There is no single, unified platform that combines live stock data, risk-return analysis, correlation insights, and performance tracking — in a format accessible to both technical analysts and business stakeholders.**

Specifically:
- Raw stock data from APIs is **unstructured and hard to analyse**
- Existing tools are either too expensive (Bloomberg) or too basic (Google Finance)
- Analysts waste hours manually pulling data into Excel every day
- Risk metrics like Sharpe Ratio and Volatility are rarely visualised together
- No single report serves both a **data analyst** (Python/SQL) and a **manager** (Excel/dashboard)

### Solution
Build an **end-to-end Real-Time Stock Market Analytics Platform** that:

1. **Automatically fetches** live price data from Yahoo Finance API
2. **Cleans and structures** it into analysis-ready datasets
3. **Calculates key metrics** — Annualised Return, Volatility, Sharpe Ratio, Correlations
4. **Visualises insights** through 6 Python charts + 1 interactive HTML dashboard
5. **Delivers a stakeholder report** via a 5-tab formatted Excel workbook

### Target Users
| User | What They Get |
|---|---|
| **Data Analyst** | Python scripts, CSVs, risk metrics, correlation matrix |
| **Portfolio Manager** | Excel report with risk-return table and monthly heatmap |
| **Business Stakeholder** | HTML live dashboard with KPIs and ticker tape |
| **Developer** | Clean, documented, GitHub-ready codebase |

### Key Questions Answered
1. Which stock has the **best risk-adjusted return** (Sharpe Ratio)?
2. Which stocks are **highly correlated** — reducing portfolio diversification?
3. What are the **seasonal patterns** in monthly returns?
4. Which stocks are **high risk vs low risk** based on annualised volatility?
5. How does each stock's **performance trend** over a rolling 30-day window?

### Impact
- Saves **2–3 hours daily** of manual data collection
- Enables **data-driven portfolio decisions** instead of gut-feel investing
- Provides a **reusable pipeline** — just run `fetch_live_data.py` each morning for fresh data
- Demonstrates **full-stack data analyst skills**: API → Python → SQL-ready → Excel → Dashboard

---

## 🗂 Project Structure

```
stock_project/
├── fetch_live_data.py          ← Step 1: Pull live data from Yahoo Finance
├── stock_analysis.py           ← Step 2: Python EDA + 6 analysis charts
├── build_excel.py              ← Step 3: Build Excel report
├── Stock_Live_Dashboard.html   ← Step 4: Open in browser for live dashboard
├── data/
│   ├── stock_history.csv       ← Historical OHLCV data (1 year, 2,610 rows)
│   ├── latest_snapshot.csv     ← Latest prices + 52W high/low metrics
│   └── stock_stats.csv         ← Risk/return statistics per ticker
├── charts/                     ← Auto-generated PNG charts (dark theme)
│   ├── chart1_normalised_performance.png
│   ├── chart2_monthly_heatmap.png
│   ├── chart3_risk_return.png
│   ├── chart4_correlation.png
│   ├── chart5_price_volume.png
│   └── chart6_rolling_sharpe.png
└── reports/
    └── Stock_Market_Analytics.xlsx   ← 5-tab Excel report
```

---

## 🚀 Quick Start

### Step 1: Install dependencies
```bash
pip install yfinance pandas matplotlib seaborn openpyxl
```

### Step 2: Fetch live data
```bash
python3 fetch_live_data.py
```

### Step 3: Run analysis & generate charts
```bash
python3 stock_analysis.py
```

### Step 4: Build Excel report
```bash
python3 build_excel.py
```

### Step 5: Open dashboard
Open `Stock_Live_Dashboard.html` in your browser — no server needed!

---

## 📊 What's Included

| Deliverable | Contents |
|---|---|
| **Live Dashboard** | Ticker tape, KPIs, 9 interactive charts, stock table, sector breakdown |
| **Python Analysis** | 6 dark-themed charts: normalised returns, heatmap, risk-return, correlation, OHLCV, rolling Sharpe |
| **Excel Report** | 5 sheets: Market Overview, Risk & Performance, Monthly Returns, Charts, Raw Data |
| **SQL-ready Data** | CSV exports ready for PostgreSQL/SQLite loading |
| **Live Data Fetcher** | One script to refresh all data from Yahoo Finance every morning |

---

## 📈 Analysis Techniques Used

- **Normalised Price Performance** — Compare all stocks on equal footing (Base = 100)
- **Monthly Returns Heatmap** — Visualise seasonality and performance patterns
- **Risk-Return Scatter (Sharpe)** — Identify best risk-adjusted investments
- **Correlation Matrix** — Understand diversification and co-movement
- **Rolling 30-Day Sharpe Ratio** — Track risk-adjusted performance over time
- **Annualised Volatility** — Measure true investment risk per stock
- **52-Week High/Low** — Understand price range and momentum

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| **Python** (pandas, numpy) | Data wrangling & analysis |
| **matplotlib, seaborn** | Chart generation |
| **yfinance** | Yahoo Finance live data API |
| **openpyxl** | Excel report generation |
| **Chart.js** | Interactive HTML dashboard |
| **HTML5 / CSS3** | Dashboard UI (no framework needed) |

---

## 📦 Dataset Summary

| Metric | Value |
|---|---|
| Stocks Tracked | 10 (AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, JPM, JNJ, V, WMT) |
| Data Points | 2,610 rows |
| Date Range | 1 Year (rolling, updates on each fetch) |
| Fields | Ticker, OHLCV, Daily Return, Beta, Sector, 52W High/Low |
| Null Values | 0 |
| OHLCV Violations | 0 |

---

## 💡 How to Make It Truly Real-Time

Schedule `fetch_live_data.py` to run every morning:

**On Mac/Linux (cron job):**
```bash
# Run every weekday at 9:00 AM
0 9 * * 1-5 python3 /path/to/stock_project/fetch_live_data.py
```

**On Windows (Task Scheduler):**
- Open Task Scheduler → Create Basic Task
- Set trigger: Daily at 9:00 AM
- Set action: `python3 fetch_live_data.py`

---

*Built as an Advanced Data Analyst Portfolio Project · Real-Time · End-to-End · Production Ready*
