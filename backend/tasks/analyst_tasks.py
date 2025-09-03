# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from tools.analyst_tools import get_llm_analysis
# from uuid import UUID

# @celery.task
# def run_llm_analysis(job_id: str):
#     db = SessionLocal()
#     job = None
#     try:
#         job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#         if not job or not job.result:
#             raise ValueError("Job not found or has no initial data.")

#         job.status = "ANALYZING" # New status for the frontend
#         db.commit()

#         current_data = job.result
#         ticker = current_data.get("ticker")
#         company_name = current_data.get("company_name")
#         intelligence_briefing = current_data.get("intelligence_briefing", {})
        
#         llm_report_data = get_llm_analysis(ticker, company_name, intelligence_briefing)
        
#         new_result = current_data.copy()
#         new_result['llm_analysis'] = llm_report_data
#         job.result = new_result
        
#         job.status = "SUCCESS"
#         db.commit()
        
#         print(f"LLM analysis for job {job_id} completed successfully.")

#     except Exception as e:
#         print(f"Error during LLM analysis for job {job_id}: {e}")
#         if job:
#             job.status = "FAILED"
#             error_data = job.result if job.result else {}
#             error_data['error'] = f"LLM analysis failed: {str(e)}"
#             job.result = error_data
#             db.commit()
#     finally:
#         db.close()










# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from tools.analyst_tools import get_llm_analysis
# from uuid import UUID

# @celery.task
# def run_llm_analysis(job_id: str):
#     with SessionLocal() as db:
#         job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#         if not job or not job.result:
#             print(f"Job {job_id} not found or has no data for analyst.")
#             return

#         try:
#             job.status = "ANALYZING"
#             db.commit()

#             current_data = job.result
#             ticker = current_data.get("ticker")
#             company_name = current_data.get("company_name")
#             intelligence_briefing = current_data.get("intelligence_briefing", {})
            
#             llm_report_data = get_llm_analysis(ticker, company_name, intelligence_briefing)
            
#             new_result = dict(current_data)
#             new_result['llm_analysis'] = llm_report_data
#             job.result = new_result
            
#             job.status = "SUCCESS"
#             db.commit()
            
#             print(f"LLM analysis for job {job_id} completed successfully.")
#             return "LLM analysis successful."
#         except Exception as e:
#             print(f"Error during LLM analysis for job {job_id}: {e}")
#             job.status = "FAILED"
#             error_data = job.result if job.result else {}
#             error_data['error'] = f"LLM analysis failed: {str(e)}"
#             job.result = error_data
#             db.commit()
#             return f"LLM analysis failed: {e}"











from celery_worker import celery
from tools.analyst_tools import get_llm_analysis

@celery.task
def get_llm_analysis_task(full_job_result: dict):
    print(f"Executing get_llm_analysis_task...")
    ticker = full_job_result.get("ticker")
    company_name = full_job_result.get("company_name")
    intelligence_briefing = full_job_result.get("intelligence_briefing", {})
    return get_llm_analysis(ticker, company_name, intelligence_briefing)