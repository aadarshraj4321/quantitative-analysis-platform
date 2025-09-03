import yfinance as yf
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any
import time

def get_llm_analysis(ticker: str, company_name: str, intelligence_briefing: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uses Gemini 1.5 Flash to analyze historical data and news to generate
    a forecast and a complete investment thesis.
    """
    print(f"Starting LLM-powered analysis for {ticker} with Gemini 1.5 Flash...")

    # clean and format ticker properly
    original_ticker = ticker
    if not ticker.endswith(('.NS', '.BO', '.L', '.TO')):
        # For Indian stocks, try NSE first
        ticker = f"{ticker}.NS"
        print(f"Formatted ticker from '{original_ticker}' to '{ticker}' for Yahoo Finance")

    historical_data_text = "Could not fetch historical price data due to repeated errors."
    
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}/3 to download historical data for {ticker}...")
            stock_data = yf.download(ticker, period="100d", interval="1d", progress=False)
            
            if not stock_data.empty:
                # Convert to a more readable format for the LLM
                stock_data = stock_data.round(2)  # Round to 2 decimal places
                # Include only the last 20 days for LLM context efficiency
                recent_data = stock_data.tail(20)
                historical_data_text = f"Recent 20 days of data for {ticker}:\n{recent_data.to_string()}"
                print("-> Successfully downloaded historical data.")
                break
            else:
                raise ValueError("Downloaded data is empty.")
                
        except Exception as e:
            print(f"-> Attempt {attempt + 1} failed: {e}")
            # If NSE fails, try BSE
            if attempt == 0 and ticker.endswith('.NS'):
                ticker = f"{original_ticker}.BO"
                print(f"Retrying with BSE ticker: {ticker}")
            elif attempt < 2:
                print("   Waiting 2 seconds before retrying...")
                time.sleep(2)

    # If all attempts failed, check if we can get basic info
    if "Could not fetch historical price data" in historical_data_text:
        try:
            print("Attempting to get basic stock info as fallback...")
            stock = yf.Ticker(ticker)
            info = stock.info
            if info and info.get('regularMarketPrice'):
                current_price = info.get('regularMarketPrice')
                previous_close = info.get('previousClose', current_price)
                historical_data_text = f"Limited data available for {ticker}:\nCurrent Price: ₹{current_price}\nPrevious Close: ₹{previous_close}"
                print("-> Got basic stock info as fallback.")
            else:
                print("-> No data available from any source.")
        except Exception as e:
            print(f"-> Fallback also failed: {e}")

    # 2. Summarize the news data into a simple text block
    articles = intelligence_briefing.get('articles', [])
    if articles:
        news_summary = "\n".join([f"- {article['title']} (Source: {article['source']}, Sentiment: {article['sentiment']})" for article in articles[:10]])  # Limit to 10 articles
    else:
        news_summary = "No recent news or social media mentions found."

    # 3. Initialize the LLM
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        return {"error": f"Failed to initialize Gemini API: {str(e)}"}

    # 4. Enhanced prompt that handles missing data gracefully
    prompt = PromptTemplate(
        input_variables=["ticker", "company_name", "historical_data", "news_summary"],
        template="""
        You are a Senior Financial Analyst for an Indian market-focused investment fund.
        Your task is to provide a comprehensive analysis and a 30-day forecast for the stock: {ticker} ({company_name}).
        
        **Important Instructions:**
        - If historical data is limited or unavailable, focus your analysis on news sentiment and general market conditions
        - Always provide a forecast range even with limited data, but adjust confidence accordingly
        - Base your analysis ONLY on the provided data

        **Data Provided:**

        1.  **Historical Price Data:**
            ```
            {historical_data}
            ```

        2.  **Recent News & Social Media Headlines:**
            {news_summary}

        **Your Analysis Report (in Markdown format):**

        ## 30-Day Price Forecast

        **Analysis:** Analyze available data (price trends if available, news sentiment, market conditions). If price data is limited, focus on sentiment analysis and sector trends.

        **Predicted Range:** Provide a realistic price range for 30 days (e.g., ₹1500 - ₹1650). If no current price available, state "Unable to provide specific range due to data limitations."

        **Justification:** Explain your forecast based on available information.

        **Confidence:** High/Moderate/Low based on data quality and availability.

        ## Investment Thesis

        **Bull Case:**
        - Point 1 based on positive signals from available data
        - Point 2 based on news sentiment or market conditions
        - Point 3 if sufficient data available

        **Bear Case:**
        - Point 1 based on negative signals or risks
        - Point 2 based on market concerns
        - Point 3 if sufficient data available

        ## Actionable Strategy

        **Signal:** Buy/Sell/Hold (choose one)

        **Strategy:** Provide 1-2 sentences with specific actionable advice based on the analysis above.

        **Risk Management:** Brief note on stop-loss or position sizing if relevant.
        """
    )

    # 5. Run the LangChain chain with error handling
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        response = chain.run(
            ticker=ticker,
            company_name=company_name,
            historical_data=historical_data_text,
            news_summary=news_summary
        )
        print("Successfully generated analysis from Gemini.")
        return {"llm_report": response}
    except Exception as e:
        error_msg = f"Failed to generate analysis from Gemini: {str(e)}"
        print(f"Error calling Gemini API: {e}")
        return {"error": error_msg}