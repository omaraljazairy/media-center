from django.apps import AppConfig
from .tasks import check_queue, play_queued_songs

class AlarmclockConfig(AppConfig):
    name = 'alarmclock'
