import pandas as pd
import yfinance as yf

# Load the symbol map from CSV
df = pd.read_csv("nse_symbols.csv")  # CSV must be in same folder

def find_symbol(company_name):
    matches = df[df['Company Name'].str.contains(company_name, case=False, na=False)]
    if matches.empty:
        return None
    elif len(matches) == 1:
        return matches.iloc[0]['Symbol']
    else:
        print("🔍 Multiple matches found:")
        for i, row in matches.iterrows():
            print(f"{i}: {row['Company Name']} → {row['Symbol']}")
        choice = int(input("Select a match by index: "))
        return matches.iloc[choice]['Symbol']

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        print(f"\n📈 {info.get('shortName', 'N/A')} ({ticker})")
        print(f"💰 Price: ₹{info.get('currentPrice', 'N/A')}")
        print(f"📊 P/E Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"🏢 Sector: {info.get('sector', 'N/A')}")
        print(f"📦 Market Cap: ₹{info.get('marketCap', 'N/A'):,}")
        print(f"🌱 EPS: {info.get('trailingEps', 'N/A')}")
        print(f"📅 52W Range: {info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')}")
    except Exception as e:
        print("❌ Error fetching data:", e)

if __name__ == "__main__":
    name = input("Enter company name (e.g., Infosys, Reliance): ")
    symbol = find_symbol(name)
    if symbol:
        get_stock_info(symbol)
    else:
        print("❌ No matching company found.")
