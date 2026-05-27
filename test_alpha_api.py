import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

print(f"API Key: {api_key[:5]}...{api_key[-5:]}")
print("\nTesting Alpha Vantage API...")

ticker = 'AAPL'
params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': ticker,
    'outputsize': 'compact',  # Use compact first
    'apikey': api_key
}

resp = requests.get('https://www.alphavantage.co/query', params=params, timeout=10)
data = resp.json()

print(f"\nResponse keys: {list(data.keys())}")
print(f"\nFull response:\n{json.dumps(data, indent=2)[:500]}...")
