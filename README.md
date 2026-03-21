# Stock-market-analytics-project
An end-to-end Real-Time Stock Market Analytics Platform tracking 10 major stocks (AAPL, MSFT, GOOGL, NVDA, TSLA &amp; more) — Live Yahoo Finance API, Python EDA, 6 Analysis Charts, Interactive HTML Dashboard &amp; 5-Tab Excel Report. Built for Data Analyst portfolios.

## Overview Tab
<img width="1366" height="634" alt="2026-03-21 (2)" src="https://github.com/user-attachments/assets/30717365-a0d8-489e-98a5-415a301b6a42" />

Displays a 1-year price chart for AAPL (Apple Inc.) with MA50, MA200, SPY, and rolling volatility overlays. Key metrics shown: current price $194.83, daily change -1.13%, Sharpe Ratio 0.59, 30-day volatility 26.7%, max drawdown -21.3%, and CAGR +21.1%. A Risk vs Return scatter plot on the right compares 10 US equities against the SPY benchmark. Live insights ticker highlights key signals like TSLA's -55.1% drawdown and fat-tail risk warnings.

## Risk Analytics Tab
<img width="1366" height="636" alt="2026-03-21 (3)" src="https://github.com/user-attachments/assets/df0cb0d1-9f74-4cd2-adbd-d14ee68fb28d" />

Shows a Drawdown Timeline for all 10 tracked equities from March 2024 to February 2025, with TSLA hitting nearly -55%. A Rolling 30-Day Volatility chart tracks annualized volatility, with TSLA and NVDA spiking highest at ~60-65%. The insights banner notes CVaR 95% extreme day risk is 33% worse than standard VaR estimates. Additional Risk Metrics Heatmap and VaR vs CVaR sections are available below.

## Monte Carlo Tab
<img width="1366" height="628" alt="2026-03-21 (4)" src="https://github.com/user-attachments/assets/fd30dd04-54c5-4645-a257-48ad088b929c" />

Displays a 200-path, 30-day forward price simulation for AAPL starting from ~$194.83. Three forecast bands are shown: bull case (90th percentile) reaching ~$215-217, median (P50) at ~$196-197, and bear case (10th percentile) declining to ~$180. The insights ticker flags that 4 of 6 tech stocks have kurtosis > 5, meaning standard VaR models underestimate tail risk. Golden cross signals are also noted for TSLA, JNJ, and V.

## Portfolio Tab
<img width="1366" height="638" alt="2026-03-21 (5)" src="https://github.com/user-attachments/assets/eed79d50-8c68-4b20-bcf7-c6c7614df753" />

Shows optimized portfolio construction with a Max Sharpe donut chart displaying weight distribution across 10 equities. A Strategy Comparison bar chart contrasts Equal Weight (+11.1%, Sh 0.61), Max Sharpe (+27.4%, Sh 2.50), Min Variance (+13.6%, Sh 1.23), and SPY Benchmark (+8.6%, Sh 0.35). Preset strategy buttons allow quick switching between optimization approaches. A Custom Portfolio Builder section is available below for manual weight adjustments.
