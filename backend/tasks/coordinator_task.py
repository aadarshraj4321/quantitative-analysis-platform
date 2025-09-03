from celery_worker import celery
from core.database import SessionLocal
from models.analysis_job import AnalysisJob
from uuid import UUID

@celery.task(bind=True)
def coordinator_task(self, results, job_id: str):
    """
    This task receives the results from all previous tasks, assembles the
    final result, and saves it to the database ONCE.
    """
    print(f"Coordinator task started for job {job_id}...")
    with SessionLocal() as db:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
        if not job:
            print(f"Job {job_id} not found in coordinator.")
            return

        try:
            # results[0] is from get_data_task
            # results[1] is from get_intelligence_task
            # results[2] is from get_llm_analysis_task
            
            final_result = {
                **results[0], # Unpack the dictionary from the data task
                "intelligence_briefing": results[1],
                "llm_analysis": results[2],
            }

            job.result = final_result
            job.status = "SUCCESS"
            db.commit()
            print(f"Coordinator task for job {job_id} successfully saved final result.")
        except Exception as e:
            print(f"Error in coordinator for job {job_id}: {e}")
            job.status = "FAILED"
            job.result = {"error": f"Final assembly failed: {str(e)}"}
            db.commit()