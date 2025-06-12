import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.tasks"]
)

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "fetch-daily-data": {
        "task": "src.tasks.fetch_data",
        "schedule": crontab(hour=0, minute=0), 
    },
}