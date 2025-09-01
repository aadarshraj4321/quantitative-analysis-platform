from celery_worker import celery
from core.database import SessionLocal
from models.analysis_job import AnalysisJob
from tools.data_tools import get_stock_data
from uuid import UUID

@celery.task
def run_data_analysis(job_id: str, ticker: str):
    db = SessionLocal()
    job = None 
    try:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
        if not job:
            print(f"Job {job_id} not found in database.")
            return

        print(f"Starting data analysis for job {job_id}, ticker {ticker}...")
        job.status = "RUNNING"
        db.commit()

        data = get_stock_data(ticker)

        job.result = data
        job.status = "SUCCESS"
        db.commit()
        print(f"Data analysis for job {job_id} completed successfully.")
        
        # get the result BEFORE closing the session
        final_result = str(job.result)

    except Exception as e:
        print(f"Error during data analysis for job {job_id}: {e}")
        if job: 
            job.status = "FAILED"
            job.result = {"error": str(e)}
            db.commit()
        final_result = f"Error: {e}"
    finally:
        # always close the database session
        db.close()

    # return the variable that is no longer attached to the session
    return final_result