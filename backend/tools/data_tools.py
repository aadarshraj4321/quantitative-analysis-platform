import yfinance as yf
from typing import Dict, Any

def get_stock_data(ticker: str) -> Dict[str, Any]:

    # for NSE stocks, yfinance expects the '.NS' suffix. For BSE, it's '.BO'.
    # assume NSE by default if no suffix is provided.
    if not ticker.endswith(('.NS', '.BO')):
        print(f"Ticker '{ticker}' has no exchange suffix. Assuming NSE and appending '.NS'.")
        ticker = f"{ticker}.NS"

    stock = yf.Ticker(ticker)
    
    # yfinance can sometimes fail for certain tickers or data points.
    try:
        info = stock.info
    except Exception as e:
        print(f"Could not fetch info for {ticker}: {e}")
        return {"error": f"Invalid ticker or no data available for {ticker}"}

    # check if we got a valid response
    if not info or info.get('regularMarketPrice') is None:
         return {"error": f"Invalid ticker or no data available for {ticker}"}

    # select key data points relevant to analysis
    data = {
        "ticker": ticker,
        "company_name": info.get('longName'),
        "current_price": info.get('currentPrice') or info.get('regularMarketPrice'),
        "previous_close": info.get('previousClose'),
        "market_cap": info.get('marketCap'),
        "pe_ratio": info.get('trailingPE') or info.get('forwardPE'),
        "pb_ratio": info.get('priceToBook'),
        "dividend_yield": info.get('dividendYield'),
        "sector": info.get('sector'),
        "industry": info.get('industry'),
        "summary": info.get('longBusinessSummary'),
        "website": info.get('website'),
        "logo_url": info.get('logo_url')
    }
    
    # clean up data by removing any keys with none values
    return {k: v for k, v in data.items() if v is not None}