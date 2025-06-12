import requests
from .celery_app import celery_app
from .database import SessionLocal
from .crud import save_fetched_data 

@celery_app.task
def fetch_data():
    db = SessionLocal()
    try:
        resp = requests.get("https://example.com/data")
        resp.raise_for_status()
        data = resp.json()
        save_fetched_data(db, data)
    finally:
        db.close()
