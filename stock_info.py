import yfinance as yf
import pandas as pd

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)

    try:
        info = stock.info
        print(f"\n📈 Stock: {info.get('shortName', 'N/A')} ({ticker})")
        print(f"💰 Current Price: ₹{info.get('currentPrice', 'N/A')}")
        print(f"📊 P/E Ratio (TTM): {info.get('trailingPE', 'N/A')}")
        print(f"🏢 Sector: {info.get('sector', 'N/A')}")
        print(f"📦 Market Cap: ₹{info.get('marketCap', 'N/A'):,}")
        print(f"🌱 EPS: {info.get('trailingEps', 'N/A')}")
        print(f"📅 52W Range: {info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')}")
    except Exception as e:
        print("❌ Error fetching data:", e)

if __name__ == "__main__":
    ticker = input("Enter NSE stock symbol (e.g. RELIANCE.NS, INFY.NS): ")
    get_stock_info(ticker)
