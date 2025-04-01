import os
import random
import time
import logging

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celeryskeleton.settings")
app = Celery('celeryskeleton')
app.config_from_object('django.conf:settings', namespace='CELERY')

logger = logging.getLogger(__name__)

@app.task(bind=True)
def raiseexceptiontask(self):
    myint = random.randint(1, 5)
    if myint != 1:
        time.sleep(60)
        raise self.retry(exc=Exception(myint), countdown=10, max_retries=7)
    else:
        print("Task completed successfully")


@app.task(bind=True)
def apply_async_task(self):
    logger.error("async")
    sleep_task.apply_async()

@app.task(bind=True)
def sleep_task(self):
    logger.error("start sleep")
    time.sleep(5)
    logger.error("end sleep")


@app.task(bind=True, max_retries=10, autoretry_for=(Exception,), retry_backoff=True)
def exponential(self):
    myint = random.randint(3, 15)
    if myint != 3:
        time.sleep(5)
        raise Exception("Something went wrong!")
    else:
        print("Task completed successfully")


@app.task(bind=True)
def test_1(self):
    logger.debug("Start sleep")
    time.sleep(30)
    logger.debug("End sleep")