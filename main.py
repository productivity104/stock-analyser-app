from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import yfinance as yf
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load your symbol CSV
df = pd.read_csv("nse_symbols.csv")

def find_symbol(company_name):
    matches = df[df['Company Name'].str.contains(company_name, case=False, na=False)]
    return matches.iloc[0]['Symbol'] if not matches.empty else None

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        "name": info.get("shortName", "N/A"),
        "price": info.get("currentPrice", "N/A"),
        "pe": info.get("trailingPE", "N/A"),
        "eps": info.get("trailingEps", "N/A"),
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "range": f"{info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')}"
    }

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def get_data(request: Request, company: str = Form(...)):
    symbol = find_symbol(company)
    if symbol:
        data = get_stock_data(symbol)
    else:
        data = {
            "name": "Not found", "price": "", "pe": "", "eps": "",
            "sector": "", "market_cap": "", "range": ""
        }
    return templates.TemplateResponse("index.html", {"request": request, "result": data})

@app.get("/screener", response_class=HTMLResponse)
async def screener_page(request: Request):
    results = []
    for symbol in df["Symbol"]:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            pe = info.get("trailingPE")
            if pe is not None:
                results.append({
                    "company": info.get("shortName", "N/A"),
                    "symbol": symbol,
                    "price": info.get("currentPrice", "N/A"),
                    "pe": pe,
                    "eps": info.get("trailingEps", "N/A"),
                    "sector": info.get("sector", "N/A"),
                })
        except Exception:
            continue

    sorted_results = sorted(results, key=lambda x: x["pe"])[:5]
    return templates.TemplateResponse("screener.html", {"request": request, "results": sorted_results})
