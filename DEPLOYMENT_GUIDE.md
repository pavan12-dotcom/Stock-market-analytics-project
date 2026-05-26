# Netlify Deployment Guide

## Quick Deploy to Netlify

### Option 1: Deploy via Netlify UI (Recommended)

1. **Go to Netlify**
   - Visit https://app.netlify.com
   - Sign up or log in with your GitHub account

2. **Connect GitHub Repository**
   - Click "New site from Git"
   - Select "GitHub" as your Git provider
   - Authorize Netlify to access your GitHub account
   - Select the `Stock-market-analytics-project` repository

3. **Configure Build Settings**
   - **Build command**: (leave empty - static site)
   - **Publish directory**: `.` (root directory)
   - Click "Deploy site"

4. **Your site will be live!**
   - Netlify will generate a unique URL (e.g., `https://stock-market-analytics-xxxx.netlify.app`)
   - Any future pushes to `main` branch will auto-deploy

### Option 2: Deploy via Netlify CLI

```bash
# Install Netlify CLI (if not already installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Navigate to project directory
cd Stock-market-analytics-project

# Deploy
netlify deploy --prod
```

## Dashboard Features

- **Live Stock Prices**: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, JPM, JNJ, V, WMT
- **Risk-Return Analysis**: Bubble chart with Sharpe ratios
- **Correlation Matrix**: Heat map showing stock relationships
- **Monthly Returns**: Historical performance breakdown
- **Interactive Charts**: Normalized performance, sector analysis
- **Real-time Data**: Updated daily from Yahoo Finance (when run locally)

## Project Structure

```
├── Stock_Live_Dashboard.html     # Main interactive dashboard
├── stock_analysis.py             # Python analysis engine
├── fetch_live_data.py            # Yahoo Finance data fetcher
├── build_excel.py                # Excel report generator
├── README.md                      # Project documentation
├── netlify.toml                   # Netlify configuration
├── charts/                        # Generated analysis charts
│   ├── chart1_normalised_performance.png
│   ├── chart2_monthly_heatmap.png
│   ├── chart3_risk_return.png
│   ├── chart4_correlation.png
│   ├── chart5_price_volume.png
│   └── chart6_rolling_sharpe.png
└── data/                          # Stock data files
    ├── stock_history.csv
    ├── stock_stats.csv
    └── latest_snapshot.csv
```

## After Deployment

1. **Custom Domain** (Optional)
   - Go to Site settings → Domain management
   - Add your custom domain

2. **Environment Variables** (Optional)
   - Site settings → Build & deploy → Environment
   - Add API keys or config values

3. **Continuous Deployment**
   - Every push to `main` branch auto-deploys
   - View deploy logs in Netlify dashboard

## Local Development

```bash
# Run Python analysis (generates latest data)
python stock_analysis.py --offline

# View locally in browser
# Open: file:///path/to/Stock_Live_Dashboard.html

# Or use HTTP server
python -m http.server 8000
# Visit: http://localhost:8000/Stock_Live_Dashboard.html
```

## Troubleshooting

- **Site not loading**: Check if `Stock_Live_Dashboard.html` exists in root directory
- **Assets not loading**: Ensure all relative paths are correct in HTML
- **Data not updating**: Run `python fetch_live_data.py` locally to refresh data

## Support

For issues, visit: https://github.com/pavan12-dotcom/Stock-market-analytics-project/issues
