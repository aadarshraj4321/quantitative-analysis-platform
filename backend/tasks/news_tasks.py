from celery_worker import celery
from tools.news_tools import get_combined_news_and_sentiment

@celery.task
def get_intelligence_task(ticker: str, company_name: str):
    print(f"Executing get_intelligence_task for {company_name}...")
    return get_combined_news_and_sentiment(ticker, company_name)