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
def play_queued_songs():
    logger.debug("running the alarmclock played_queue_songs")
    from .queueprocessor import QueueProcesser
    queue_processor = QueueProcesser()
    queue_processor.play_queued_songs()
    logger.debug("finnished the alarmclock played_queue_songs")

@app.task
def check_queue():
    logger.debug("running the alarmclock check_queue")
    from .queueprocessor import QueueProcesser
    queue_processor = QueueProcesser()
    queue_processor.set_queued_songs()
    logger.debug("finished the alarmclock check_queue")

