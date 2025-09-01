from celery import Celery
from core.config import settings

# giving app a more descriptive name
celery = Celery(
    "quantitative_analysis_platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.data_tasks", "tasks.news_tasks"] 
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

