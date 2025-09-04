from celery_worker import celery
from tools.analyst_tools import get_llm_analysis

@celery.task
def get_llm_analysis_task(full_job_result: dict):
    print(f"Executing get_llm_analysis_task...")
    ticker = full_job_result.get("ticker")
    company_name = full_job_result.get("company_name")
    intelligence_briefing = full_job_result.get("intelligence_briefing", {})
    return get_llm_analysis(ticker, company_name, intelligence_briefing)