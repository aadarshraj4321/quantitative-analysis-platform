import yfinance as yf
from prophet import Prophet
import pandas as pd
from typing import Dict, Any

def generate_forecast(ticker: str) -> Dict[str, Any]:
    print(f"Generating forecast for ticker {ticker}...")
    
    stock_data = yf.download(ticker, period="2y", progress=False)
    
    if stock_data.empty:
        return {"error": f"Could not download historical data for {ticker}."}

    # --- THE FINAL, MOST ROBUST FIX FOR THE DATAFRAME ---
    # 1. Create a new DataFrame with only the columns we need.
    df_prophet = stock_data[['Close']].copy()
    # 2. Reset the index to turn the 'Date' index into a column.
    df_prophet.reset_index(inplace=True)
    # 3. Rename the columns to what Prophet expects.
    df_prophet.columns = ['ds', 'y']
    # --- END OF FIX ---

    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05
    )
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    current_price = df_prophet['y'].iloc[-1]
    predicted_price_30_days = forecast['yhat'].iloc[-1]
    trend = "upward" if predicted_price_30_days > current_price else "downward"
    change_percent = ((predicted_price_30_days - current_price) / current_price) * 100

    forecast_data = {
        "summary": (
            f"The model predicts a {trend} trend over the next 30 days. "
            f"Current price: {current_price:.2f}, "
            f"predicted price in 30 days: {predicted_price_30_days:.2f} "
            f"({change_percent:+.2f}% change)."
        ),
        # Convert datetime objects to strings for JSON compatibility
        "history_plot_data": [
            {'ds': r['ds'].isoformat(), 'y': r['y']} for r in df_prophet.tail(90).to_dict('records')
        ],
        "forecast_plot_data": [
            {
                'ds': r['ds'].isoformat(),
                'yhat': r['yhat'],
                'yhat_lower': r['yhat_lower'],
                'yhat_upper': r['yhat_upper']
            } for r in forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(120).to_dict('records')
        ]
    }
    
    print(f"Forecast for {ticker} generated successfully.")
    return forecast_data