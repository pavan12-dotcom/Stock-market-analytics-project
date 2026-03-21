# Stock Analytics Terminal v3.0
### A Data Analysis Project on US Equity Markets

> An interactive stock market analytics dashboard built to analyze, visualize, and derive insights from historical US equity data using statistical and financial analysis techniques.



---

##  Problem Statement

Investors and analysts struggle to make sense of stock market data without tools that go beyond basic price charts. Raw stock data alone doesn't reveal **hidden risks, volatility patterns, portfolio inefficiencies, or future price uncertainty**. Most free tools lack advanced risk metrics like CVaR, drawdown analysis, or portfolio optimization — making it difficult for data-driven decision-making. This project addresses that gap by building a comprehensive stock analytics dashboard that transforms raw market data into **actionable financial insights**.

---

##  Solution

This project analyzes **10 major US equities** benchmarked against the **SPY (S&P 500 ETF)** across a 1-year period. Using Python-based data analysis and interactive JavaScript visualizations, the dashboard delivers:

 **Price & Trend Analysis** — Historical price charts with Moving Averages (MA50, MA200) and SPY comparison
 **Risk Analytics** — Drawdown timelines, rolling volatility, VaR 95%, CVaR 95%, and a risk heatmap
 **Monte Carlo Simulation** — 200-path, 30-day price forecasting using Geometric Brownian Motion
 **Portfolio Optimization** — Max Sharpe, Min Variance, and Equal Weight strategy comparison
 **Auto Insights** — Automated alerts for golden crosses, tail risks, kurtosis anomalies, and Sharpe signals

---

## Dashboard Screenshots

### 1. Overview Tab
Displays a 1-year price chart for AAPL with MA50, MA200, SPY overlay, and rolling volatility. Key metrics include current price ($194.83), Sharpe Ratio (0.59), 30-day volatility (26.7%), max drawdown (-21.3%), and CAGR (+21.1%). A Risk vs Return scatter plot compares all 10 equities visually against the SPY benchmark.

![Overview](<img width="1366" height="634" alt="2026-03-21 (2)" src="https://github.com/user-attachments/assets/eb594416-8c9c-4e92-aa5c-fa40f3ca3ee3" />
)

---

### 2. Risk Analytics Tab
Shows a Drawdown Timeline and Rolling 30-Day Volatility chart across all 10 stocks from March 2024 to February 2025. TSLA recorded the worst drawdown at nearly -55%, while TSLA and NVDA showed the highest volatility spikes (~60-65%). CVaR 95% analysis reveals extreme day losses are 33% worse than standard VaR estimates.

![Risk Analytics](<img width="1366" height="636" alt="2026-03-21 (3)" src="https://github.com/user-attachments/assets/789fb774-d6ff-4e0a-b785-623eca809ba0" />
)

---

### 3. Monte Carlo Simulation Tab
Runs 200 simulated price paths over a 30-day forecast horizon for AAPL using Geometric Brownian Motion. Results show a bull case (90th percentile) of ~$215-217, a median (P50) of ~$196-197, and a bear case (10th percentile) of ~$180. Kurtosis analysis flags 4 of 6 tech stocks with fat-tail risk beyond normal distribution assumptions.

![Monte Carlo](<img width="1366" height="628" alt="2026-03-21 (4)" src="https://github.com/user-attachments/assets/1dd99239-8973-46b6-8768-28801c8245e2" />
)

---

### 4. Portfolio Optimization Tab
Compares four portfolio strategies — Equal Weight (+11.1%, Sharpe 0.61), Max Sharpe (+27.4%, Sharpe 2.50), Min Variance (+13.6%, Sharpe 1.23), and SPY Benchmark (+8.6%, Sharpe 0.35). The Max Sharpe allocation donut chart shows optimal weight distribution. A Custom Portfolio Builder allows manual weight adjustment with real-time metric updates.

![Portfolio](<img width="1366" height="638" alt="2026-03-21 (5)" src="https://github.com/user-attachments/assets/674f19ea-ac68-4259-9b80-b302688adf09" />
)

---

##  Technologies Used

### Data Analysis & Statistics
| Tool / Library | Purpose |
|---|---|
| **Python** | Core data analysis and scripting language |
| **Pandas** | Data cleaning, manipulation, and time-series analysis |
| **NumPy** | Numerical computations, returns, and matrix operations |
| **SciPy** | Portfolio optimization via quadratic programming |
| **Statsmodels** | Statistical modeling and regression analysis |

### Data Collection
| Tool / Library | Purpose |
|---|---|
| **yfinance** | Fetching historical stock price data from Yahoo Finance |
| **Pandas DataReader** | Pulling financial data from public APIs |

### Visualization
| Tool / Library | Purpose |
|---|---|
| **Matplotlib** | Static charts for EDA and analysis reports |
| **Seaborn** | Heatmaps and statistical distribution plots |
| **Plotly** | Interactive financial charts and dashboards |
| **Chart.js** | Frontend interactive charts (price, bar, scatter) |
| **D3.js** | Custom risk vs return scatter plot visualization |

### Financial & Risk Models
| Model / Method | Purpose |
|---|---|
| **Sharpe Ratio** | Measures risk-adjusted return |
| **Sortino Ratio** | Penalizes only downside volatility |
| **VaR 95% (Value at Risk)** | Maximum expected loss on 95% of trading days |
| **CVaR 95% (Conditional VaR)** | Average loss on the worst 5% of days |
| **Max Drawdown & Calmar Ratio** | Peak-to-trough loss measurement |
| **Rolling 30-Day Volatility** | Time-varying risk tracking across stocks |
| **Kurtosis Analysis** | Fat-tail detection beyond normal distribution |
| **Golden Cross Detection** | MA50 crossing above MA200 as bullish signal |
| **Geometric Brownian Motion** | Stochastic model for Monte Carlo price simulation |
| **Modern Portfolio Theory** | Markowitz mean-variance optimization framework |

### Portfolio Optimization Strategies
| Strategy | Description |
|---|---|
| **Equal Weight** | 10% allocation to each of the 10 equities |
| **Max Sharpe (Optimised)** | Maximizes risk-adjusted return via optimization |
| **Min Variance** | Minimizes portfolio volatility using covariance matrix |
| **SPY Benchmark** | S&P 500 ETF used as the market performance baseline |

### Tools & Environment
| Tool | Purpose |
|---|---|
| **Jupyter Notebook** | Exploratory Data Analysis (EDA) and reporting |
| **VS Code** | Development environment |
| **Git & GitHub** | Version control and project hosting |
| **HTML / CSS / JavaScript** | Interactive dashboard frontend |

---

##  Key Metrics Explained

| Metric | Description |
|---|---|
| **Sharpe Ratio** | Return per unit of total risk (higher = better) |
| **Sortino Ratio** | Like Sharpe, but only penalizes downside risk |
| **VaR 95%** | Worst expected daily loss 95% of the time |
| **CVaR 95%** | Average loss in the worst 5% of trading days |
| **Max Drawdown** | Largest peak-to-trough decline in the period |
| **Calmar Ratio** | Annualized return divided by max drawdown |
| **CAGR** | Compound Annual Growth Rate over the period |
| **Kurtosis** | Measures fat tails; values > 5 signal extreme risk |
| **Rolling Volatility** | 30-day annualized standard deviation of returns |
| **Golden Cross** | Bullish signal when MA50 crosses above MA200 |

---

##  Stocks Analyzed

| Ticker | Company |
|---|---|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corp. |
| GOOGL | Alphabet Inc. |
| AMZN | Amazon.com Inc. |
| TSLA | Tesla Inc. |
| NVDA | NVIDIA Corp. |
| JPM | JPMorgan Chase |
| JNJ | Johnson & Johnson |
| V | Visa Inc. |
| WMT | Walmart Inc. |
| **SPY** | **S&P 500 ETF (Benchmark)** |

---

##  Project Structure

```
stock-analytics-terminal/
├── data/
│   ├── raw/                  # Raw downloaded stock price CSVs
│   └── processed/            # Cleaned and transformed data
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_analysis.ipynb
│   ├── 03_risk_metrics.ipynb
│   ├── 04_portfolio_optimization.ipynb
│   └── 05_monte_carlo.ipynb
├── dashboard/
│   ├── index.html
│   ├── css/terminal.css
│   └── js/
│       ├── priceChart.js
│       ├── riskCharts.js
│       ├── monteCarlo.js
│       └── portfolioCharts.js
├── screenshots/
│   ├── screenshot-overview.png
│   ├── screenshot-risk-analytics.png
│   ├── screenshot-monte-carlo.png
│   └── screenshot-portfolio.png
├── requirements.txt
└── README.md
```

---

##  How to Run

```bash
# Clone the repository
git clone https://github.com/your-username/stock-analytics-terminal.git
cd stock-analytics-terminal

# Install Python dependencies
pip install -r requirements.txt

# Run notebooks in order
jupyter notebook notebooks/01_data_collection.ipynb

# Launch the dashboard (open in browser)
open dashboard/index.html
```

**requirements.txt**
```
pandas
numpy
scipy
yfinance
matplotlib
seaborn
plotly
statsmodels
jupyter
```

---

##  Key Insights from Analysis

-  **TSLA** recorded the worst drawdown at **-55.1%** with kurtosis **6.8**, indicating fat-tail risk **2x** a normal distribution
-  **MSFT** offered the best risk-adjusted return among all equities on the Risk vs Return scatter plot
-  **Max Sharpe portfolio** delivered **+27.4% return** with a Sharpe of **2.50** vs SPY's **+8.6%** at Sharpe **0.35**
-  **CVaR 95%** showed extreme losses are **33% worse** than standard VaR estimates across the portfolio
-  **AMZN and V** showed negative Sharpe ratios, underperforming the risk-free rate on a risk-adjusted basis
-  **Golden Cross signals** detected recently in TSLA, JNJ, and V — a bullish technical indicator

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

##  Acknowledgements

- Market data sourced via [yfinance](https://pypi.org/project/yfinance/) (Yahoo Finance)
- Portfolio optimization based on **Modern Portfolio Theory** (Markowitz, 1952)
- SPY ETF used as S&P 500 market benchmark

---

> 📌 *This project is built for educational and analytical purposes only. Not financial advice.*
