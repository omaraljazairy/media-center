from .scheduler import Scheduler
from .models import QueuedSongs, PlayedSongs
from django.db import IntegrityError
from mediacenter.player import Player
from django.utils import timezone
import logging
import os
from django.conf import settings
MEDIA_FILES = getattr(settings, "MEDIA_ROOT", None)

logger = logging.getLogger('processor')
scheduler = Scheduler()

class QueueProcesser():

    ''' this class sets the alarms in the scheduledSongs table and moves the played songs to the PlayedSongs table '''
    

#    def __init__(self):
#        ''' the initializer will check first if there are available schedules alarms '''
#        self.alarms = scheduler.get_scheduled_alarms()
#        logger.debug("alarms available to be processed in the queue : %s", len(self.alarms))

#        ''' if alarms found, it will call the set_queued_songs to add the songs of the alarms in the queue '''
#        if len(self.alarms) > 0:
#            self.set_queued_songs()
#        else:
#            logger.debug("no scheduled alarms available to be processed")


    def set_queued_songs(self):
        ''' gets the available alarms of the day and sets them in the queue '''
        logger.debug("setting the queue")

        alarms = scheduler.get_scheduled_alarms()
        logger.debug("alarms available to be processed in the queue : %s", len(alarms))
        ''' 
        if alarms found, it will it will call the get_alarm_details to start processing the the scheduled alarms. 

        '''

        if len(alarms) > 0: # if there are alarms found .
            ''' 
            if there are alarms found, I will get the details (dict object) of the found alarms from the alarms object i received 
            from the Scheduler. then I will add the songs listed per alarm in the queue and update the Alarm executed column 
            with the current datetime. 

            '''

            alarm_details = scheduler.get_alarm_details(alarms)
            logger.debug("alarm_details: %s", alarm_details)

            for i in range(0,len(alarms)): # loop through the alarms to get the songs and add themin the queue
                logger.debug("alarm_id: %s to be queued", str(alarms[i].id))
                
                logger.debug("there are :%s songs to be queued", len(alarm_details[i]['songs']))
                for song in alarm_details[i]['songs']: # taking the songs of each alarm and adding it to the queue
                    logger.debug("songid : %s to be queued", song)
                    qs = QueuedSongs(alarm=alarm_details[i]['id'],song_id=song,scheduled=alarm_details[i]['schedule_datetime'])

                    try:
                        qs.save()
                        alarms[i].executed = timezone.now() # updating the Alarm executed column with the current datetime
                        alarms[i].save()
                        logger.debug("alarm saved")
                    except IntegrityError as e:
                        logger.error("exception : error saving :%s", e.__cause__)

        else: # no scheduled alarms found
            logger.debug("no scheduled alarms available to be processed")





    def set_played_songs(self):
        ''' move the played songs in the queue to the playedsongs table '''

        logger.info("set_played_songs started")
        played_queued_songs = QueuedSongs.objects.exclude(played__isnull = True) # find all the songs in the queue except played is null
        
        if played_queued_songs: 

            for ps in played_queued_songs:
                logger.debug("played songs found: song_id %s, alarm_id: %s, played: %s", ps.song_id, ps.alarm_id,ps.played)
                ''' save all the found played songs in the queue in the PlayedSongs object '''

                playedsongs = PlayedSongs(alarm_id=ps.alarm_id,song_id=ps.song_id, played=ps.played)

                try:
                    playedsongs.save() # save the songs in the PlayedSongs table
                    logger.debug("playedqueued songs saved to the playedsongs")
                    ps.delete() # delete the played song from the queuedsongs table
                    logger.debug("playedsongs deleted from the queue")

                except IntegrityError as e:
                    logger.error("exception : error saving :%s", e.__cause__)



        else:
            logger.debug("no played songs found which need to be played at or before : %s", str(timezone.now()))


    def play_queued_songs(self):
        ''' gets all the songs which haven't been played in the queue and now() > scheduled '''
        
        player = Player() # creating the player object
        ''' check if the playeris already busy playing a song '''
 
        if player.is_busy():
            msg = "player isbusy playing a song"
            logger.info("player isbusy playing a song")
            return msg
        else:
            logger.debug("getting the queued songs where their scheduled time is lte %s",str(timezone.now()))
            available_songs = QueuedSongs.objects.get_queryset().get_current_queued_alarms() # objects.filter(scheduled__lte=timezone.now(),played__isnull = True)
            logger.debug("available_songs: %s", len(available_songs))

            if available_songs:

                queue = list(available_songs) # creating a list to contain all the queued songs
                logger.debug("queue: %s",queue)
                logger.debug("there are %s songs found scheduled to be played", len(available_songs))
                
                i = 1 # creating a counter for the logger
                for data in available_songs: # getting the data from the available songs

                    if str(data.song.file).endswith('mp3'): # searching only for files with extension mp3 
                        
                        logger.debug('queueid: %s, song: %s, filename: %s', data.id, data.song, data.song.file)
                        file = os.path.join(MEDIA_FILES, str(data.song.file))  # adding the file path to the file name

                        logger.info("song number: %s sent to the player to be played", i)
                        player.play({'name': data.song, 'file': file}) # sending the song and the file to the player object to play the song

                        self.update_played_queue_item(data.id) # updating the playedsong in the queue
                        i += 1 # incrementing the counter

                self.set_played_songs() # callign this function to delete the played songs
                logger.debug("no songs left in the queue to be played at or before : %s", str(timezone.now()))
            else:
                logger.debug("no songs found available in the queue to be played at or before : %s", str(timezone.now()))


    def update_played_queue_item(self,queueid):
        ''' this function will update the played timestamp to now() based on the queueid it receives '''

        updated_queue_id = QueuedSongs.objects.filter(id=queueid).update(played=timezone.now())
        logger.debug("updated queueid: %s => %s", queueid, updated_queue_id)
