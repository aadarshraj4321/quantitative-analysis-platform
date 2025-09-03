# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from tools.data_tools import get_stock_data
# from uuid import UUID

# @celery.task
# def run_data_analysis(job_id: str, ticker: str):
#     db = SessionLocal()
#     job = None
#     final_result = ""
#     try:
#         job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#         if not job:
#             raise ValueError(f"Job {job_id} not found in database.")

#         print(f"Status - DATA_FETCHING for job {job_id}...")
#         job.status = "DATA_FETCHING"
#         db.commit()

#         data = get_stock_data(ticker)
        
#         if "error" in data:
#             raise ValueError(data["error"])

#         job.result = data
#         db.commit()
#         print(f"Data analysis for job {job_id} completed successfully.")
        
#         final_result = str(job.result)

#     except Exception as e:
#         print(f"Error during data analysis for job {job_id}: {e}")
#         if job:
#             job.status = "FAILED"
#             job.result = {"error": f"Data analysis failed: {str(e)}"}
#             db.commit()
#         final_result = f"Error: {e}"
#     finally:
#         db.close()

#     return final_result







# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from tools.data_tools import get_stock_data
# from uuid import UUID

# @celery.task
# def run_data_analysis(job_id: str, ticker: str):
#     with SessionLocal() as db:
#         job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#         if not job:
#             print(f"Job {job_id} not found.")
#             return

#         try:
#             job.status = "DATA_FETCHING"
#             db.commit()

#             data = get_stock_data(ticker)
#             if "error" in data:
#                 raise ValueError(data["error"])

#             job.result = data
#             db.commit()
#             print(f"Data analysis for job {job_id} completed successfully.")
#             return "Data fetching successful."
#         except Exception as e:
#             print(f"Error during data analysis for job {job_id}: {e}")
#             job.status = "FAILED"
#             job.result = {"error": f"Data analysis failed: {str(e)}"}
#             db.commit()
#             return f"Data fetching failed: {e}"









from celery_worker import celery
from tools.data_tools import get_stock_data

@celery.task
def get_data_task(ticker: str):
    print(f"Executing get_data_task for {ticker}...")
    return get_stock_data(ticker)