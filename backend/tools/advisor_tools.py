from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any
import json

def generate_investment_thesis(full_job_result: Dict[str, Any]) -> str:
    """
    Uses the Gemini 1.5 Flash model to generate a qualitative investment thesis.
    """
    print("Generating investment thesis with Gemini 1.5 Flash...")

    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Create a simplified summary of the data to pass to the LLM
    # This prevents sending thousands of characters of raw data
    fundamentals_summary = (
        f"Company: {full_job_result.get('company_name', 'N/A')}\n"
        f"Current Price: {full_job_result.get('current_price', 'N/A')}\n"
        f"Market Cap: {full_job_result.get('market_cap', 'N/A')}\n"
        f"P/E Ratio: {full_job_result.get('pe_ratio', 'N/A'):.2f}\n"
        f"Sector: {full_job_result.get('sector', 'N/A')}"
    )
    
    prediction_summary = full_job_result.get('prediction_analysis', {}).get('summary', 'No prediction summary available.')
    
    # We need to handle the case where intelligence gathering might have failed
    intelligence_briefing = full_job_result.get('intelligence_briefing', {})
    if intelligence_briefing and intelligence_briefing.get('news'):
        news_summary = ", ".join([f"'{article['title']}' ({article['sentiment']})" for article in intelligence_briefing['news'][:2]])
    else:
        news_summary = "No news articles found."

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["fundamentals", "prediction", "news"],
        template="""
        You are a sharp, concise senior financial analyst for an Indian market-focused fund.
        Your task is to provide a clear investment thesis based on the data provided.
        Do not offer financial advice. Analyze the data objectively.

        **Data Overview:**
        - **Fundamentals:** {fundamentals}
        - **Quantitative Forecast:** {prediction}
        - **Recent News Headlines & Sentiment:** {news}

        **Your Analysis (in Markdown format):**
        **1. Executive Summary:** A 2-sentence summary of the company's current situation based on the data.
        **2. Bull Case:** 2-3 bullet points on the positive signals from the data.
        **3. Bear Case:** 2-3 bullet points on the primary risks or negative signals.
        **4. Final Recommendation:** State ONE of the following: 'Strong Buy', 'Buy', 'Hold', 'Sell', or 'Strong Sell' and provide a brief 1-sentence justification based purely on the provided data mix.
        """
    )

    # Create the LangChain chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain with our summarized data
    try:
        response = chain.run(
            fundamentals=fundamentals_summary,
            prediction=prediction_summary,
            news=news_summary
        )
        print("Successfully generated thesis from Gemini.")
        return response
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error: Could not generate the advisor summary."