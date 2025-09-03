from celery_worker import celery
from core.database import SessionLocal
from models.analysis_job import AnalysisJob
from tools.prediction_tools import generate_forecast
from uuid import UUID

@celery.task
def run_prediction_analysis(job_id: str):
    db = SessionLocal()
    job = None
    final_result = ""
    try:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
        if not job or not job.result:
            raise ValueError(f"Job {job_id} not found or has no initial data.")

        print(f"Status - PREDICTING for job {job_id}...")
        job.status = "PREDICTING"
        db.commit()

        current_data = job.result
        ticker = current_data.get("ticker")
        if not ticker:
            raise ValueError("Ticker not found in initial data.")
        
        forecast_data = generate_forecast(ticker)
        
        if "error" in forecast_data:
            raise ValueError(forecast_data["error"])

        new_result = current_data.copy()
        new_result['prediction_analysis'] = forecast_data
        job.result = new_result
        
        db.commit()
        
        print(f"Prediction analysis for job {job_id} completed successfully.")
        final_result = str(job.result)

    except Exception as e:
        print(f"Error during prediction analysis for job {job_id}: {e}")
        if job:
            job.status = "FAILED"
            error_data = job.result if job.result else {}
            error_data['error'] = f"Prediction analysis failed: {str(e)}"
            job.result = error_data
            db.commit()
        final_result = f"Error: {e}"
    finally:
        db.close()
            
    return final_result