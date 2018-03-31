from .scheduler import Scheduler
from .models import QueuedSongs, PlayedSongs
from django.db import IntegrityError
from mediacenter.player import Player
import datetime
import logging
import sys,os
from django.conf import settings
MEDIA_FILES = getattr(settings, "MEDIA_ROOT", None)

logger = logging.getLogger('processor')

class QueueProcesser():

    ''' this class sets the alarms in the scheduledSongs table and moves the played songs to the PlayedSongs table '''
    alarms = [] # a list of all available alarms for today.

    def __init__(self):

        scheduler = Scheduler()
        logger.debug("message from scheduer: %s", scheduler.available_alarms)
        self.play_queued_songs()
        if scheduler.available_alarms:

            self.alarms = scheduler.available_alarms

            logger.debug("available alarms: %s", self.alarms)
            self.set_queued_songs()
            self.set_played_songs()
        else:
            logger.debug("no scheduled alarms available to be processed")


    def set_queued_songs(self):
        ''' gets the available alarms of the day and sets them in the queue '''
        logger.debug("setting the queue")
        logger.debug("there are :%s alarms available", len(self.alarms))


        for i in range(0,len(self.alarms)):
            logger.debug("alarm: %s with id: %s to be queued", i, self.alarms[i]['id'])
            logger.debug("there are :%s songs to be queued", len(self.alarms[i]['songs']))
            for song in self.alarms[i]['songs']:
                logger.debug("songid : %s to be queued", song)
                qs = QueuedSongs(alarm=self.alarms[i]['id'],song_id=song,scheduled=self.alarms[i]['schedule_datetime'])
                try:
                    qs.save()
                    logger.debug("alarm saved")
                except IntegrityError as e:
                    logger.error("exception : error saving :%s", e.__cause__)



    def set_played_songs(self):
        ''' move the played songs in the queue to the playedsongs table '''

        logger.info("set_played_songs started")
        played_queued_songs = QueuedSongs.objects.exclude(played__isnull = True)
        if played_queued_songs:

            for ps in played_queued_songs:
                logger.debug("played songs found: song_id %s, alarm_id: %s, played: %s", ps.song_id, ps.alarm_id,ps.played)
                playedsongs = PlayedSongs(alarm_id=ps.alarm_id,song_id=ps.song_id, played=ps.played)
                played_queued_songs = QueuedSongs.objects.get(id=ps.id)
                try:
                    playedsongs.save()
                    logger.debug("playedqueued songs saved to the playedsongs")
                    played_queued_songs.delete()
                    logger.debug("playedsongs deleted from the queue")

                except IntegrityError as e:
                    logger.error("exception : error saving :%s", e.__cause__)



        else:
            logger.debug("no played songs found")


    def play_queued_songs(self):
        ''' gets all the songs which haven't been played in the queue and now() > scheduled '''
        logger.debug("getting the queued songs where their scheduled time is lte %s",str(datetime.datetime.now()))
        available_songs = QueuedSongs.objects.filter(scheduled__lte=datetime.datetime.now(),played__isnull = True)
        logger.debug("available_songs: %s", available_songs.count())

        if available_songs.count():

            queue = list(available_songs)
            logger.debug("queue: %s",queue)
            logger.debug("there are %s songs found scheduled to be played", available_songs.count())
            player = Player()
            i = 1
            for data in available_songs:
                if str(data.song.file).endswith('mp3'):
                    logger.debug('queueid: %s, song: %s, filename: %s', data.id, data.song, data.song.file)
                    file = os.path.join(MEDIA_FILES, str(data.song.file))  # adding the file path to the file name
                    logger.info("song number: %s sent to the player to be played", i)
                    play_song = player.play({'name': data.song, 'file': file})
                    logger.debug("play_song return %s", play_song)
                    self.update_played_queue_item(data.id)
                    i += 1

            self.set_played_songs()
            logger.debug("no songs left in the queue")
        else:
            logger.debug("there are no songs to be played in the queue")


    def update_played_queue_item(self,queueid):
        ''' this function will update the played timestamp to now() based on the queueid it receives '''

        updated_queue_id = QueuedSongs.objects.filter(id=queueid).update(played=datetime.datetime.now())
        logger.debug("updated queueid: %s => %s", queueid, updated_queue_id)
