# Stock Market Analytics — API & Dashboard Setup

## Quick Start Guide

### Step 1: Install Dependencies
Run the following command to install all required Python packages:

```bash
pip install requests pandas openpyxl python-dotenv yfinance
```

### Step 2: Get Free Alpha Vantage API Key (Optional but Recommended)

**Alpha Vantage provides FREE real-time stock data:**

1. Visit: https://www.alphavantage.co/
2. Click **"GET FREE API KEY"**
3. Enter your email and get instant API key
4. **Free tier:** 5 API calls per minute (sufficient for daily updates)

### Step 3: Configure Your API Key

Create a `.env` file in the project root directory with:

```env
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

OR set as environment variable:

**Windows (PowerShell):**
```powershell
$env:ALPHA_VANTAGE_API_KEY="your_api_key_here"
```

**Linux/macOS:**
```bash
export ALPHA_VANTAGE_API_KEY="your_api_key_here"
```

### Step 4: Generate Dashboard Data

Run the data generator to fetch real stock data and update the dashboard:

```bash
python generate_dashboard_data.py
```

Or force a specific provider:
```bash
python generate_dashboard_data.py --provider alpha   # Force Alpha Vantage
python generate_dashboard_data.py --provider yahoo   # Force Yahoo Finance (free, no key needed)
```

### Step 5: View the Dashboard

Open `Stock_Live_Dashboard.html` in your web browser to see real-time stock data, charts, and analytics.

---

## Notes

- **No API key needed?** The script falls back to Yahoo Finance automatically
- **Want live updates?** Schedule the script to run daily using cron (Linux/macOS) or Task Scheduler (Windows)
- **Data caching:** Historical data is cached in `/data/` directory for faster loading

---

## Troubleshooting

### "ALPHA_VANTAGE_API_KEY not found"
- Make sure you've created the `.env` file with your API key
- Verify the key is valid at alphavantage.co

### "Rate limited"
- Alpha Vantage free tier allows 5 calls/minute
- The script has built-in delays; wait a few minutes before trying again

### "No data from any source"
- Check your internet connection
- Ensure yfinance is installed: `pip install yfinance`
