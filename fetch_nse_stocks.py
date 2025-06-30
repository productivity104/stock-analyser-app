import requests
import pandas as pd
from io import StringIO

# NSE equity listings CSV URL
url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

# Required headers to bypass NSE security
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com"
}

def fetch_nse_stocks():
    print("📥 Downloading NSE stock list...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    try:
        # Load CSV and clean column names
        df = pd.read_csv(StringIO(response.text), encoding='unicode_escape')
        df.columns = df.columns.str.strip()  # Remove spaces

        print("📊 Available columns:", df.columns.tolist())

        if "SERIES" not in df.columns:
            print("❌ 'SERIES' column not found. Saving raw for inspection.")
            df.to_csv("nse_raw_debug.csv", index=False)
            return

        # Filter only equity series
        df = df[df["SERIES"] == "EQ"]

        # Keep useful columns
        df = df[["SYMBOL", "NAME OF COMPANY"]]
        df.columns = ["Symbol", "Company Name"]
        df["Symbol"] = df["Symbol"].str.strip().str.upper() + ".NS"

        # Save cleaned data
        df.to_csv("nse_symbols.csv", index=False)
        print(f"✅ Saved {len(df)} NSE stocks to 'nse_symbols.csv'")

    except Exception as e:
        print("❌ Error processing data:", e)

if __name__ == "__main__":
    fetch_nse_stocks()
