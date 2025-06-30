import pandas as pd
import yfinance as yf

# Load company symbol list
df_symbols = pd.read_csv("nse_symbols.csv")

# Function to get data for each stock
def fetch_stock_metrics(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "Symbol": symbol,
            "Company": info.get("shortName", ""),
            "Price": info.get("currentPrice", None),
            "P/E Ratio": info.get("trailingPE", None),
            "EPS": info.get("trailingEps", None),
            "Market Cap": info.get("marketCap", None),
            "Sector": info.get("sector", "")
        }
    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")
        return None

# Fetch data for all companies
results = []
for symbol in df_symbols["Symbol"]:
    print(f"Fetching: {symbol}")
    metrics = fetch_stock_metrics(symbol)
    if metrics:
        results.append(metrics)

# Convert to DataFrame
df = pd.DataFrame(results)

# Clean up and sort
df = df.dropna(subset=["P/E Ratio"])
top_5_pe = df.sort_values(by="P/E Ratio").head(5)

# Show the top 5
print("\n🔍 Top 5 NSE Stocks with Lowest P/E Ratio:\n")
print(top_5_pe[["Company", "Symbol", "Price", "P/E Ratio", "EPS", "Sector"]])

# Optional: export to Excel
df.to_csv("screener_output.csv", index=False)
print("\n✅ All stock data saved to screener_output.csv")
