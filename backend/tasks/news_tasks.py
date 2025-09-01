from celery_worker import celery
from core.database import SessionLocal
from models.analysis_job import AnalysisJob
from tools.news_tools import get_news_and_sentiment, get_twitter_sentiment
from uuid import UUID

@celery.task
def run_intelligence_analysis(job_id: str):
    db = SessionLocal()
    job = None
    try:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
        if not job or not job.result: raise ValueError(f"Job {job_id} not found or has no data.")

        current_data = job.result
        company_name = current_data.get("company_name")
        if not company_name: raise ValueError("Company name not found in data.")

        print(f"Starting intelligence analysis for {company_name}...")
        
        news = get_news_and_sentiment(current_data.get("ticker"), company_name)
        twitter = get_twitter_sentiment(f"{company_name} stock")
        
        current_data['intelligence_briefing'] = {"news": news, "twitter": twitter}
        job.result = current_data
        job.status = "SUCCESS"
        db.commit()
        
        print(f"Intelligence analysis for job {job_id} completed.")
        final_result = str(job.result)

    except Exception as e:
        print(f"Error during intelligence analysis for job {job_id}: {e}")
        if job:
            job.status = "FAILED"
            error_data = job.result if job.result else {}
            error_data['error'] = f"Intelligence analysis failed: {str(e)}"
            job.result = error_data
            db.commit()
        final_result = f"Error: {e}"
    finally:
        db.close()
    return final_result