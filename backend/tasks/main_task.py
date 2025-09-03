# from celery_worker import celery
# from core.database import SessionLocal
# from models.analysis_job import AnalysisJob
# from tools.data_tools import get_stock_data
# from tools.news_tools import get_combined_news_and_sentiment
# from tools.analyst_tools import get_llm_analysis
# from uuid import UUID
# import json

# @celery.task
# def run_full_analysis(job_id: str, ticker: str):
#     print(f"\n--- [START] Full Analysis for Job ID: {job_id} ---")
    
#     # --- Stage 1: Data Fetching ---
#     try:
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             if not job: raise ValueError("Job not found")
#             job.status = "DATA_FETCHING"
#             db.commit()
#         print("[LOG] STATUS UPDATE: DATA_FETCHING")
        
#         data_result = get_stock_data(ticker)
#         if "error" in data_result: raise ValueError(data_result['error'])
#         company_name = data_result.get("company_name", ticker)
        
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             job.result = data_result
#             db.commit()
#             db.refresh(job) # Force reload from DB
#             print(f"[LOG] DB SAVE 1 (Data): Result keys are now: {list(job.result.keys())}")

#     except Exception as e:
#         print(f"!!! [FAILURE] Stage 1 (Data): {e}")
#         # ... error handling ...
#         return

#     # --- Stage 2: Intelligence Gathering ---
#     try:
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             job.status = "INTELLIGENCE_GATHERING"
#             db.commit()
#         print("[LOG] STATUS UPDATE: INTELLIGENCE_GATHERING")

#         intelligence_result = get_combined_news_and_sentiment(ticker, company_name)
        
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             current_result = dict(job.result)
#             current_result['intelligence_briefing'] = intelligence_result
#             job.result = current_result
#             db.commit()
#             db.refresh(job) # Force reload
#             print(f"[LOG] DB SAVE 2 (Intelligence): Result keys are now: {list(job.result.keys())}")
#     except Exception as e:
#         print(f"!!! [FAILURE] Stage 2 (Intelligence): {e}")
#         # ... error handling ...
#         return

#     # --- Stage 3: LLM Analysis ---
#     try:
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             job.status = "ANALYZING"
#             db.commit()
#         print("[LOG] STATUS UPDATE: ANALYZING")

#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             data_for_llm = job.result
        
#         llm_result = get_llm_analysis(ticker, company_name, data_for_llm.get("intelligence_briefing", {}))
#         if "error" in llm_result: raise ValueError(llm_result['error'])
        
#         # --- Final Assembly and Save ---
#         print("[LOG] Finalizing results...")
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             final_result_data = dict(job.result)
#             final_result_data['llm_analysis'] = llm_result
#             job.result = final_result_data
#             job.status = "SUCCESS"
#             db.commit()
#             db.refresh(job)
#             print(f"[LOG] DB SAVE 3 (Final): Result keys are now: {list(job.result.keys())}")
        
#         print(f"--- [SUCCESS] Full analysis for {job_id} complete. ---")

#     except Exception as e:
#         print(f"!!! [FAILURE] Stage 3 (LLM): {e}")
#         with SessionLocal() as db:
#             job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()
#             if job:
#                 job.status = "FAILED"
#                 error_data = job.result if job.result else {}
#                 error_data['error'] = str(e)
#                 job.result = error_data
#                 db.commit()










from celery_worker import celery
from core.database import SessionLocal
from models.analysis_job import AnalysisJob
from tools.data_tools import get_stock_data
from tools.news_tools import get_combined_news_and_sentiment
from tools.analyst_tools import get_llm_analysis
from uuid import UUID
import json

@celery.task
def run_full_analysis(job_id: str, ticker: str):
    """
    The single, main task that orchestrates the entire analysis pipeline.
    """
    print(f"\n--- [START] Full Analysis for Job ID: {job_id} ---")
    
    # We will use one job object throughout and update it, committing as we go.
    # This requires careful session management.
    db = SessionLocal()
    job = db.query(AnalysisJob).filter(AnalysisJob.id == UUID(job_id)).first()

    if not job:
        print(f"Job {job_id} not found. Aborting.")
        db.close()
        return

    try:
        # --- Stage 1: Data Fetching ---
        print(f"Stage 1: DATA_FETCHING for job {job_id}")
        job.status = "DATA_FETCHING"
        db.commit()
        
        data_result = get_stock_data(ticker)
        if "error" in data_result:
            raise ValueError(f"Data fetching failed: {data_result['error']}")
        
        company_name = data_result.get("company_name", ticker)
        
        job.result = data_result
        db.commit()
        print("-> Data fetching stage complete.")

        # --- Stage 2: Intelligence Gathering ---
        print(f"Stage 2: INTELLIGENCE_GATHERING for job {job_id}")
        job.status = "INTELLIGENCE_GATHERING"
        db.commit()
        
        intelligence_result = get_combined_news_and_sentiment(ticker, company_name)
        
        current_result = dict(job.result)
        current_result['intelligence_briefing'] = intelligence_result
        job.result = current_result
        db.commit()
        print("-> Intelligence gathering stage complete.")
        
        # --- Stage 3: LLM Analysis ---
        print(f"Stage 3: ANALYZING for job {job_id}")
        job.status = "ANALYZING"
        db.commit()

        # We need to refresh the job object to get the latest result for the LLM
        db.refresh(job)
        data_for_llm = job.result
        
        llm_result = get_llm_analysis(ticker, company_name, data_for_llm.get("intelligence_briefing", {}))
        if "error" in llm_result:
            raise ValueError(f"LLM analysis failed: {llm_result['error']}")
        
        # --- Final Assembly and Save ---
        print("Finalizing results for job {job_id}")
        final_result_data = dict(job.result)
        final_result_data['llm_analysis'] = llm_result
        
        job.result = final_result_data
        job.status = "SUCCESS"
        db.commit()
        
        print(f"--- [SUCCESS] Full analysis for {job_id} complete. ---")

    except Exception as e:
        error_message = str(e)
        print(f"!!! [FAILURE] Full analysis for {job_id} FAILED: {error_message}")
        if job:
            job.status = "FAILED"
            # Provide a cleaner error message for the user, while keeping technical details
            user_friendly_error = f"Analysis failed for ticker '{ticker}'. This stock may not be listed or there was a problem fetching its data. Please check the ticker symbol and try again. (Details: {error_message})"
            
            error_data = job.result if job.result else {}
            error_data['error'] = user_friendly_error
            job.result = error_data
            db.commit()
    finally:
        db.close()