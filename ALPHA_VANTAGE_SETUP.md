# 🔷 Alpha Vantage API Integration Guide

This project now supports **Alpha Vantage API** for fetching real-time stock data, with Yahoo Finance as a fallback option.

## 📋 Quick Setup

### Step 1: Install Dependencies
```bash
pip install requests python-dotenv pandas yfinance matplotlib seaborn openpyxl
```

### Step 2: Get Alpha Vantage API Key (FREE)

1. Visit: **https://www.alphavantage.co/**
2. Click **"GET FREE API KEY"**
3. Enter your email and receive instant API key
4. API Tier: **Free (5 API calls per minute)**

### Step 3: Configure API Key

**Option A: Create `.env` file (Recommended)**
```bash
# Create .env in project root
echo "ALPHA_VANTAGE_API_KEY=your_api_key_here" > .env
```

**Option B: Set Environment Variable**
```bash
# Windows PowerShell
$env:ALPHA_VANTAGE_API_KEY="your_api_key_here"

# Linux/macOS
export ALPHA_VANTAGE_API_KEY="your_api_key_here"
```

**Option C: Edit `.env` file directly**
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

---

## 🚀 Usage

### Auto-Detect Provider (Alpha Vantage first, fallback to Yahoo)
```bash
python fetch_live_data.py
```

### Force Alpha Vantage
```bash
python fetch_live_data.py --provider alpha
```

### Force Yahoo Finance
```bash
python fetch_live_data.py --provider yahoo
```

---

## 📊 Data Sources Comparison

| Feature | Alpha Vantage | Yahoo Finance |
|---------|---|---|
| **Real-time Data** | ✅ Yes | ✅ Yes |
| **Historical Data** | ✅ Up to 20 years | ✅ Up to 20 years |
| **Free API Limit** | 5 calls/min | Unlimited* |
| **API Key Required** | ✅ Yes | ❌ No |
| **Reliability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Support** | Official API | Community |

*Yahoo Finance has unofficial rate limits

---

## ⚡ Rate Limiting & Best Practices

### Free Tier Limits
- **5 API calls per minute** (non-premium)
- Each ticker = 1 API call
- Project uses 10 tickers = ~2 minutes per fetch
- Wait time is handled automatically (12 sec between calls)

### Optimization Tips
1. **Run once per day** — Stock data doesn't change every minute
2. **Use `--provider yahoo`** — If you hit rate limits, switch to Yahoo
3. **Premium Subscription** — For unlimited calls
4. **Test with `--provider demo`** — Uses demo key (limited data)

---

## 🔑 API Key Security

### Do NOT Commit `.env` to Git
```bash
# .gitignore should include:
.env
.env.local
*.env
```

Check if already added:
```bash
cat .gitignore | grep "\.env"
```

### Use Demo Key for Testing
```
ALPHA_VANTAGE_API_KEY=demo
```
Limited data but no rate limits for testing.

---

## 📈 Full Workflow

```bash
# 1. Fetch live data
python fetch_live_data.py

# 2. Regenerate analysis charts
python stock_analysis.py

# 3. Build Excel report
python build_excel.py

# 4. Open dashboard in browser
start Stock_Live_Dashboard.html
```

---

## ❓ Troubleshooting

### Error: "API key not found"
```bash
# Check if .env file exists and contains key
cat .env

# Verify environment variable
echo $ALPHA_VANTAGE_API_KEY  # Linux/macOS
echo %ALPHA_VANTAGE_API_KEY% # Windows
```

### Error: "Rate limit exceeded"
```bash
# Switch to Yahoo Finance temporarily
python fetch_live_data.py --provider yahoo

# Or wait 60 seconds before running again
```

### Error: "No data returned"
- Check if ticker symbol is correct (case-sensitive: AAPL not aapl)
- Verify API key is active (check email from Alpha Vantage)
- Try demo key first: `ALPHA_VANTAGE_API_KEY=demo`

---

## 📚 API Response Example

```json
{
  "Time Series (Daily)": {
    "2026-05-27": {
      "1. open": "189.45",
      "2. high": "192.78",
      "3. low": "188.92",
      "4. close": "191.23",
      "5. volume": "58234567"
    },
    "2026-05-26": { ... }
  }
}
```

---

## 🔗 Useful Links

- **Alpha Vantage Docs**: https://www.alphavantage.co/documentation/
- **API Key Dashboard**: https://www.alphavantage.co/manage-keys.php
- **Supported Functions**: https://www.alphavantage.co/data-api/
- **Premium Plans**: https://www.alphavantage.co/premium/

---

## 💡 Next Steps

1. ✅ Get API key from Alpha Vantage
2. ✅ Create `.env` file with your key
3. ✅ Run `python fetch_live_data.py`
4. ✅ View data in dashboard: `Stock_Live_Dashboard.html`

**Questions?** Check Alpha Vantage documentation or GitHub issues.
