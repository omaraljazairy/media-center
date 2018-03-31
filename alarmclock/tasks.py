#from __future__ import absolute_import, unicode_literals
#from celery import shared_task, task
#from celery.utils.log import get_task_logger
import logging
from mediacenter.celery import app

logger = logging.getLogger("tasks")


@app.task
def showme(x):
    logger.debug("showme_tasks: %s", x)
    return x

@app.task
def add(x,y):
    logger.debug("add_task: %s", x)
    return x + y

@app.task
def mul(x,y):
    logger.debug("mul_task: %s", x)
    return x * y

@app.task
def xsum(numbers):
    logger.debug("xsum_task: %s", numbers)
    return sum(numbers)

@app.task
def check_queue():
    logger.debug("running the alarmclock queue")
    from .queueprocessor import QueueProcesser
    queue_processor = QueueProcesser()
    logger.debug("found available alarms: %s", queue_processor.alarms)

