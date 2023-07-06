# from config import REDIS_URL
import time
import os

from celery import Celery
from celery.schedules import crontab
from fastapi import Depends
# from database import get_async_session
os.chdir('/Users/vladislavtrofimov/PycharmProjects/market_place_fastapi/')

celery_app = Celery(__name__,include=["workers.tasks"])



celery_app.conf.timezone = 'UTC'
celery_app.conf.broker_url = 'redis://localhost:6379/0'

celery_app.conf.beat_schedule = {
 "check_expiring": {
     "task": "check_expiring",
     "schedule": 5,

 }
}
celery_app.autodiscover_tasks()

celery_app.control.purge()
celery_app.conf.timezone = 'UTC'
celery_app.conf.update(task_track_started=True)
celery_app.conf.result_backend = "redis://localhost:6379/0"