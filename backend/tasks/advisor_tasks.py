from celery_worker import celery
from core.database import SessionLocal
from models.analysis_job import AnalysisJob
from tools.advisor_tools import generate_investment_thesis
from uuid import UUID

@celery.task
def run_advisor_analysis(job_id: str):
    db = SessionLocal()
    job = None
    final_result = ""
    try:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
        if not job or not job.result:
            raise ValueError(f"Job {job_id} not found or has no result data for the advisor.")
        
        print(f"Status - SUMMARIZING for job {job_id}...")
        job.status = "SUMMARIZING"
        db.commit()

        current_data = job.result
        
        advisor_summary = generate_investment_thesis(current_data)
        
        new_result = current_data.copy()
        new_result['advisor_summary'] = advisor_summary
        job.result = new_result
        
        job.status = "SUCCESS" # This is the final successful step
        db.commit()
        
        print(f"Advisor analysis for job {job_id} completed successfully.")
        final_result = str(job.result)

    except Exception as e:
        print(f"Error during advisor analysis for job {job_id}: {e}")
        if job:
            job.status = "FAILED"
            error_data = job.result if job.result else {}
            error_data['error'] = f"Advisor analysis failed: {str(e)}"
            job.result = error_data
            db.commit()
        final_result = f"Error: {e}"
    finally:
        db.close()
        
    return final_result