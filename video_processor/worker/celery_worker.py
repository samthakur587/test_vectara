from celery import Celery
# from app.config import *
from app.tasks import *

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
# app.config_from_object('config')

if __name__ == '__main__':
    app.start()