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

@app.task(
    bind=True,
    max_retries=3,
    retry_backoff=120,
    retry_backoff_max=480 + 1,
    retry_jitter=False,
    autoretry_for=(Exception,)
)
def task_with_auto_retry(self):
    print("Start task " + self.request.id)
    myint = random.randint(1, 5)
    if myint != 1:
        time.sleep(60)
        raise Exception("Something went wrong!")
    else:
        print("Task completed successfully")

@app.task(bind=True)
def test_3(self):
    try:
        print("Start task" + self.request.id)
        myint = random.randint(1, 5)
        if myint != 1:
            time.sleep(60)
            raise Exception("Something went wrong!")
        else:
            print("Task completed successfully!!")
    except Exception as exc:
        raise self.retry(
            exc=exc,
            countdown=((self.request.retries + 1) * 120),  # Exponential backoff, max 480 seconds
            max_retries=3
        )

@app.task(bind=True)
def test_4(self):
    try:
        raise Exception("Something went wrong!")
    except Exception as exc:
        raise self.retry(
            exc=exc,
            countdown=((self.request.retries + 1) * 1200),  # Exponential backoff, max 480 seconds
            max_retries=3
        )

@app.task(bind=True,
          max_retries=3,
          retry_backoff=120,
          retry_backoff_max=480 + 1,
          retry_jitter=False,
          autoretry_for=(Exception,)
          )
def task_with_catch(self):
    try:
        myint = random.randint(1, 5)
        if myint != 1:
            time.sleep(30)
            raise Exception("Something went wrong!")
        else:
            print("Task completed successfully")
    except Exception as exc:
        print("Caught the Exception!")
        #raise Exception Used in the second run in task 5

@app.task(bind=True,
          max_retries=3,
          retry_backoff=120,
          retry_backoff_max=480 + 1,
          retry_jitter=False,
          autoretry_for=(Exception,)
          )
def test_6(self):
    myint = random.randint(1, 5)
    if myint != 1:
        time.sleep(30)
        test = 1 / 0
    else:
        time.sleep(30)
        print("Task was successful!")

@app.task(
    bind=True,
    max_retries=2,
    retry_backoff=120,
    retry_jitter=False,
    autoretry_for=(Exception,)
)
def task_without_ack(self):
    print("Start a new task")
    myint = random.randint(1, 5)
    if myint != 1:
        print("Task has failed!")
        time.sleep(120)
        raise Exception("Raising exception!!")
    else:
        time.sleep(30)
        print("Task was successful!")

@app.task(
    max_retries=2,
    retry_backoff=120,
    retry_jitter=False,
    autoretry_for=(Exception,)
)
def task_without_bind():
    myint = random.randint(1,6)
    if myint != 6:
        print('Task has failed!')
        time.sleep(60)
        raise Exception('Exception!')
    else:
        print('Task was successful!')
        time.sleep(10)

@app.task(
    bind=True,
    rate_limit="2/m",
)
def task_with_rate_limit(self):
    print("Start task" + self.request.id)

@app.task(
    bind=True,
    rate_limit="1/m",
    max_retries=3,
    retry_backoff=120,
    retry_jitter=False,
    autoretry_for=(Exception,),
)
def task_with_rate_limit_and_retry(self):
    myint = random.randint(1, 5)
    if myint != 1:
        print('Task has failed!')
        raise Exception("Raising exception!!")
    else:
        print("Task was successful!")

@app.task(
    track_started=True,
    bind=True,
    max_retries=3,
    retry_backoff=120,
    retry_jitter=False,
    autoretry_for=(Exception,),
    queue="TroubleshootingCelery-dlq",
)
def task_with_retry_on_diff_queue(self):
    myint = random.randint(1, 5)
    if myint != 1:
        print('Task has failed!')
        time.sleep(30)
        raise Exception("Raising exception!!")
    else:
        print("Task was successful!")
        time.sleep(10)

@app.task(
    bind=True,
    track_started=True,
    max_retries=3,
    retry_backoff=60,
    retry_backoff_max=480 +1,
    retry_jitter=(1),
    autoretry_for=(Exception,),
)
def task_with_jitter(self):
    print("Starting Task")
    time.sleep(5)
    raise Exception('This is an exception')

@app.task(bind=True,
          max_retries=3,
          retry_backoff=120,
          retry_backoff_max=120 + 1,
          retry_jitter=False,
          autoretry_for=(Exception,)
          )
def long_running_task(self):
    print('Start a long-running task')
    time.sleep(240)
    print('End the long-running task')