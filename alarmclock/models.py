from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from library.models import Artist, Playlist,  Song
from mediacenter.utils import Choices
from multiselectfield import MultiSelectField
from django.urls import reverse
from operator import xor
from datetime import datetime
import logging
from .validators import validate_artist, validate_playlist
from django.utils import timezone


logger = logging.getLogger('alarmclock')


def validate_day(days):
    logger.info("days given : %s", days)


class AlarmsQuerySet(models.query.QuerySet):

    def available_alarms(self,date):
        ''' get the total available active alarms '''

        return self.filter(Q(day__contains = date['day']) | Q(daily = True), active=True).exclude( executed__date = timezone.now())


class AlarmsManager(models.Manager):

    def get_queryset(self):

        return AlarmsQuerySet(self.model, using=self._db)        


class Alarms(models.Model):
    '''
    this model contains the schedules for the alarms only.
    The scheduler will execute the scheduled alarms and add the songs in the queue.
    '''

    days_daily_err_msg = "Either daily option is selected or a weekday."
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
    )


    name        = models.CharField(max_length=30, null=False, unique=True)
    day         = MultiSelectField(max_length=100, choices=DAY_CHOICES, null=True, blank=True)
    daily       = models.BooleanField(default=False)
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
    executed    =   models.DateTimeField(auto_now=False, default='2018-01-01 00:00:00', db_index=True)
    objects     =   AlarmsManager()


    class Meta:

        ordering = ('updated',)
        verbose_name_plural = "Alarms" #used for the admin tool to show the name of the modelwithout the s
        unique_together = ('day', 'hour')
        unique_together = ('daily', 'hour')


    def get_absolute_url(self):
        ''' this is required for the update and delete views '''
        return reverse('alarmclock:alarm_details',kwargs={'pk':self.pk})


    def __str__(self):
        return self.name

    def clean(self):

        '''
        Here I will check the values of the daily option and the days.
        if both are True or False, it will raise an exception on the daily field.
        one of the fieldsshould be True only
        '''

        logger.debug("day : %s", self.day)
        logger.debug("daily : %s", self.daily)
        if xor(self.daily, bool(len(self.day))) == False:
            logger.error("msg : %s", self.days_daily_err_msg)
            raise ValidationError({'daily':self.days_daily_err_msg}) #assiging the error to the daily field.
        else:
            logger.debug("the daily_day validator passed")

class QueuedSongsQuerySet(models.query.QuerySet):
    ''' this queryset has one function which gives the current queued alarms in the queue object '''

    def get_current_queued_alarms(self):
        ''' this function takes no arguments and returns a queryset of queued alarms which arenot processed '''

        return self.filter(scheduled__lte=timezone.now(),played__isnull = True)


class QueuedSongsManager(models.Manager):
    ''' this class hasone methd which gives back the QuerySet object class '''

    def get_queryset(self):
        ''' this function returns the queueryset object '''

        return QueuedSongsQuerySet(self.model, using=self._db)


class QueuedSongs(models.Model):
    '''
    the queue processor will get all the songs from the scheduledsongs and add them in this model.
    when the song is played, it will have the played column set to now().
    when all the songs are playedin the queue, they willbe moved to the PlayedSongs model
    '''

    alarm = models.ForeignKey(
        Alarms,
        on_delete=models.CASCADE,
        related_name='queued_alarm',
    )

    scheduled   = models.DateTimeField(auto_now_add=False, db_index=True)

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='queued_song'
    )

    played  = models.DateTimeField(auto_now_add=False,verbose_name="Song played time", db_index=True, null=True)
    objects = QueuedSongsManager()


    class Meta:

        ordering = ('scheduled',)
        verbose_name_plural = 'QueuedSongs'
        unique_together = ('alarm', 'song')

    def __str__(self):
        return str(self.scheduled.strftime('%Y-%m-%d %H:%M:%S'))


class PlayedSongsManager(models.Manager):

    ''' this manager holds all the queries needed from the PlayedSongs objects '''

    def get_todays_played_alarms(self):
        ''' this function returns a list of all the alarm_ids played in the current day '''
        i = datetime.now()
        return self.filter(played__gte=i.strftime('%Y-%m-%d 00:00:00')).values_list('alarm_id')


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
    played      = models.DateTimeField(auto_now_add=False,verbose_name="Song played time", db_index=True)

    added       = models.DateTimeField(auto_now=True, verbose_name="song added")
    objects     = PlayedSongsManager()

    class Meta:
        ordering = ('played',)
        verbose_name_plural = "PlayedSongs"

    def __str__(self):
        return str(self.played)
