import os
import random
import time

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celeryskeleton.settings")
app = Celery('celeryskeleton')
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task(bind=True)
def raiseexceptiontask(self):
    myint= random.randint(1,5);
    if myint != 1:
        time.sleep(60)
        raise self.retry(exc=Exception(myint), countdown=10, max_retries=7)
    else:
        print("Task completed successfully")


raiseexceptiontask.delay()
