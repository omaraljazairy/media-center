from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from celery import shared_task
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE','mediacenter.settings')
app = Celery('mediacenter') #, broker='redis://192.168.192.26:6379/0', backend='redis')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
'add-every-minute-contrab': {
        'task': 'alarmclock.tasks.check_queue',
        'schedule': timedelta(minutes=1),
        'args': (),
    },
}

'''
app.conf.beat_schedule = {
'add-every-minute-contrab': {
        'task': 'alarmclock.tasks.add',
        'schedule': crontab(minute=1),
        'args': (16, 16),
    },
'add-every-2-minute': {
        'task': 'alarmclock.tasks.mul',
        'schedule': crontab(minute=2),
        'args': (16, 16)
    },
'add-every-3-minute': {
        'task': 'alarmclock.tasks.showme',
        'schedule': crontab(minute=3),
        'args': (1,)
    },
}
'''