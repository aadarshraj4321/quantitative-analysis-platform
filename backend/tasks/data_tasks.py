from celery_worker import celery
from tools.data_tools import get_stock_data

@celery.task
def get_data_task(ticker: str):
    print(f"Executing get_data_task for {ticker}...")
    return get_stock_data(ticker)