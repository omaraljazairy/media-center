from django.apps import AppConfig
from .tasks import showme, add, mul, xsum

class AlarmclockConfig(AppConfig):
    name = 'alarmclock'
