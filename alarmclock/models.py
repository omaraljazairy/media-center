from django.db import models
from library.models import Artist, Playlist,  Song
from mediacenter.utils import Choices
from multiselectfield import MultiSelectField
from django.urls import reverse
import logging
from .validators import validate_days, validate_artist, validate_playlist

logger = logging.getLogger('alarmclock')


def validate_day(days):
    logger.info("days given : %s", days)


class Alarms(models.Model):
    '''
    this model contains the schedules for the alarms only.
    The scheduler will execute the scheduled alarms and add the songs in the queue.
    '''

    logger.debug("alarms model")
    class Days(Choices):
        SATURDAY    = 'Saturday'
        SUNDAY      = 'Sunday'
        MONDAY      = 'Monday'
        TUESDAY     = 'Tuesday'
        WEDNESDAY   = 'Wednesday'
        THURSDAY    = 'Thursday'
        FRIDAY      = 'Friday'
        DAILY       = 'Daily'

    DAY_CHOICES = (
        ('SATURDAY','Saturday'),
        ('SUNDAY','Sunday'),
        ('MONDAY' , 'Monday'),
        ('TUESDAY' , 'Tuesday'),
        ('WEDNESDAY' , 'Wednesday'),
        ('THURSDAY' , 'Thursday'),
        ('FRIDAY' , 'Friday'),
        ('DAILY' , 'Daily'),
    )


    name        = models.CharField(max_length=30, null=False, unique=True)
    #day         = models.CharField(max_length=100,choices=Days.choices(), null=False,default='Daily')
    day         = MultiSelectField(max_length=100, choices=DAY_CHOICES, null=False, blank=False, default='Daily', validators=[validate_days])
    hour        = models.TimeField(null=False)
    artist      = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='alarm_artist',
        null=True,
        blank=True,
        validators=[validate_artist]
    )

    playlist    = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='alarm_playlist',
        null=False,
        blank=False,
        default=0,
        validators=[validate_playlist]
    )

    total_songs =   models.IntegerField(default=1, verbose_name="total songs to be played")
    active      =   models.BooleanField(default=True)
    created     =   models.DateTimeField(auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True)



    class Meta:

        ordering = ('updated',)
        verbose_name_plural = "Alarms"
        unique_together = ('day', 'hour')


    def get_absolute_url(self):
        return reverse('alarmclock:alarm_details',kwargs={'pk':self.pk})


    def __str__(self):
        return self.name

models.signals.pre_save.connect(validate_days,sender=Alarms)

class QueuedSongs(models.Model):
    '''
    the queue processor will get all the songs from the scheduledsongs and add them in this model.
    when the song is played, it will have the played column set to now().
    when all the songs are playedin the queue, they willbe moved to the PlayedSongs model
    '''

    alarm = models.ForeignKey(
        Alarms,
        on_delete=models.CASCADE,
        related_name='queued_alarm'

    )

    scheduled   = models.DateTimeField(auto_now_add=True)

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='queued_song'
    )

    played  = models.BooleanField(default=False)

    class Meta:

        ordering = ('scheduled',)
        verbose_name_plural = 'QueuedSongs'

    def __str__(self):
        return self.scheduled


class PlayedSongs(models.Model):
    ''' All the played songs from the queue will be moved here by the processor '''

    alarm = models.ForeignKey(
        Alarms,
        on_delete=models.CASCADE,
        related_name='played_alarm'

    )

    song        = models.ForeignKey(
        Song,
        related_name='played_song',
        on_delete=models.CASCADE
    )
    played      = models.DateTimeField(verbose_name="Song played time", db_index=True)


    class Meta:
        ordering = ('played',)
        verbose_name_plural = "PlayedSongs"

    def __str__(self):
        return str(self.played)

