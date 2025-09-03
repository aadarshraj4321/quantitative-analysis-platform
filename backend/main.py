# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from uuid import UUID
# import models.analysis_job as model
# import schemas
# from core.database import SessionLocal, engine
# # Import only our single, main task
# from tasks.main_task import run_full_analysis

# # This ensures tables are created on startup (good for development)
# model.Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="Quantitative Analysis Platform API",
#     version="0.1.0",
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Dependency to get a database session for each API request
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/jobs", response_model=schemas.Job, status_code=201)
# def create_analysis_job(job_request: schemas.JobCreate, db: Session = Depends(get_db)):
#     """
#     Creates a new analysis job and dispatches the main background task.
#     """
#     db_job = model.AnalysisJob(ticker=job_request.ticker.upper())
#     db.add(db_job)
#     db.commit()
#     db.refresh(db_job)
    
#     # Dispatch our single, all-in-one analysis task to run in the background
#     run_full_analysis.delay(str(db_job.id), db_job.ticker)
    
#     # Immediately return the created job to the frontend
#     return db_job

# @app.get("/jobs/{job_id}", response_model=schemas.Job)
# def get_job_status(job_id: UUID, db: Session = Depends(get_db)):
#     """
#     Allows the frontend to poll for the status and result of an analysis job.
#     """
#     db_job = db.query(model.AnalysisJob).filter(model.AnalysisJob.id == job_id).first()
#     if db_job is None:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return db_job





from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc # Import desc for ordering
from uuid import UUID
from typing import List # Import List for the history endpoint
import models.analysis_job as model
import schemas
from core.database import SessionLocal, engine
from tasks.main_task import run_full_analysis

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quantitative Analysis Platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/jobs", response_model=schemas.Job, status_code=201)
def create_analysis_job(job_request: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = model.AnalysisJob(ticker=job_request.ticker.upper())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    run_full_analysis.delay(str(db_job.id), db_job.ticker)
    
    return db_job

@app.get("/jobs/{job_id}", response_model=schemas.Job)
def get_job_status(job_id: UUID, db: Session = Depends(get_db)):
    db_job = db.query(model.AnalysisJob).filter(model.AnalysisJob.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

# --- NEW ENDPOINT FOR HISTORY PANEL ---
@app.get("/jobs", response_model=List[schemas.Job])
def get_jobs_history(db: Session = Depends(get_db)):
    db_jobs = db.query(model.AnalysisJob).order_by(desc(model.AnalysisJob.created_at)).limit(20).all()
    return db_jobs