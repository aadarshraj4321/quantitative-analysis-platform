from celery import Celery
from core.config import settings

celery = Celery(
    "quantitative_analysis_platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    # This is the corrected list. We only have one task file now.
    include=[
        "tasks.main_task"
    ]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)