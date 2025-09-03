import yfinance as yf
from typing import Dict, Any

def get_stock_data(ticker: str) -> Dict[str, Any]:
    if not ticker.endswith(('.NS', '.BO')):
        ticker = f"{ticker}.NS"

    stock = yf.Ticker(ticker)
    
    try:
        info = stock.info
    except Exception as e:
        print(f"Could not fetch info for {ticker}: {e}")
        return {"error": f"Invalid ticker or no data available for {ticker}"}

    if not info or info.get('regularMarketPrice') is None:
         return {"error": f"Invalid ticker or no data available for {ticker}"}

    # --- UPGRADED DATA FETCHING ---
    data = {
        "ticker": ticker,
        "company_name": info.get('longName'),
        "current_price": info.get('currentPrice') or info.get('regularMarketPrice'),
        "previous_close": info.get('previousClose'),
        "day_high": info.get('dayHigh'),
        "day_low": info.get('dayLow'),
        "fifty_two_week_high": info.get('fiftyTwoWeekHigh'),
        "fifty_two_week_low": info.get('fiftyTwoWeekLow'),
        "volume": info.get('volume'),
        "average_volume": info.get('averageVolume'),
        "market_cap": info.get('marketCap'),
        "pe_ratio": info.get('trailingPE'),
        "pb_ratio": info.get('priceToBook'),
        "dividend_yield": info.get('dividendYield'),
        "sector": info.get('sector'),
        "industry": info.get('industry'),
        "summary": info.get('longBusinessSummary'),
        "website": info.get('website'),
        # Get CEO info if available
        "ceo": next((officer['name'] for officer in info.get('companyOfficers', []) if 'CEO' in officer.get('title', '')), "N/A"),
    }
    
    return {k: v for k, v in data.items() if v is not None}