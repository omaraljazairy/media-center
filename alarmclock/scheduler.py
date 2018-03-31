from datetime import datetime
from django.db.models import Q
from .models import Alarms, QueuedSongs,PlayedSongs
from library.models import PlaylistSong,  Song
from mediacenter.utils import QuerySetConverter
import logging
import random

logger = logging.getLogger('scheduler')

class Scheduler():
    ''' this class schedules the alarms set in the Alarms model
        it will do the following:
        1- read check the scheduled alarms per day (daily / currentday).
        2- creates a list of the songs from the artist and playlists set by the alarm.
        3- it will schedule the songs based on hour set in the alarm.
        4- the scheduled alarms will be saved in the queuedsongs table.
    '''

    available_alarms = None

    def __init__(self):
        logger.debug("scheduler started")
        alarms = self.get_scheduled_alarms(self.get_date_day())
        if alarms.count():
            logger.debug("alarm found: %s", alarms.count())
            scheduled_alarms = self.get_alarm_details(alarms, self.get_date_day())
            logger.debug("scheduled alarms: %s", scheduled_alarms)
            self.available_alarms = scheduled_alarms
        else:
            self.available_alarms = 0


    def get_date_day(self):
        """ setting the current day name and date and returning them in a dict """
        now = datetime.now()
        today_day = now.strftime("%A")
        today_date = datetime.today().strftime('%Y-%m-%d')
        logger.debug("today's day is : %s and date: %s", today_day, today_date)
        return {'day':today_day, 'date':today_date}




    def get_scheduled_alarms(self,date):

        """ this function searches for the available scheduled alarms and returns an alarm object"""

        queued_alarm_ids = list(QueuedSongs.objects.all().values_list('alarm_id'))
        logger.debug("queued_alarm_ids: %s", queued_alarm_ids)

        played_alarm_ids_today = list(PlayedSongs.objects.filter(played__gte=datetime.today()).values_list('alarm_id'))
        logger.debug("played_alarm_ids_today: %s",played_alarm_ids_today)
        queued_alarm_ids.extend(played_alarm_ids_today)
        logger.debug("queued_alarm_ids after extension: %s", queued_alarm_ids)
        ''' creating a list from the queued_alarm_id, converting it to a set to remove the duplicate values and put it back to list '''
        queued_alarm_id_list = list(set([i[0] for i in queued_alarm_ids]))

        logger.debug("queued_alarm_id_list before the set: %s", queued_alarm_id_list)
        logger.debug("queued_alarms type = %s and values: %s", type(queued_alarm_ids), queued_alarm_ids )
        logger.debug("queued_alarm_id_list: %s",queued_alarm_id_list)
        alarm = Alarms.objects.filter(Q(day__contains = date['day']) | Q(daily = True), active=True).exclude(id__in=queued_alarm_id_list)
        """ where clause query = where (day like %todayname% or daily = True) and active = True """
        logger.debug("alarm_ids found: %s", list(alarm.values_list('id')))
        logger.debug('total alarms found : %s', alarm.count())

        return alarm



    def get_alarm_details(self,alarm, date):
        """ get the alarm object which contains all the available scheduled alarms for currentday """

        alarm_details = [] #list to save all the song_ids

        for i in range(0,len(alarm)): #looping through the alarms


            alarm_datetime_string = date['date'] +" ".__add__(str(alarm[i].hour))
            alarm_datetime = datetime.strptime(alarm_datetime_string,'%Y-%m-%d %H:%M:%S')

            total = int(alarm[i].total_songs) #total songs
            songs = self.get_songs_from_alarm(alarm[i], total_songs=total)


            data = {
                'id':Alarms.objects.get(pk=alarm[i].id),
                'name':alarm[i].name,
                'schedule_datetime': alarm_datetime,
                'songs':songs
            }
            alarm_details.append(data)

        return alarm_details

    def get_songs_from_alarm(self,alarm, total_songs=int):


        songs_list = []

        if alarm.artist and alarm.playlist.id > 0: #only if the alarmhas a playlist AND artist set
            logger.debug("both playlist with songs and artist are selected")
            songs = Song.objects.filter(artist = alarm.artist)
            """ query clause = select * from song where artist = artist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(songs.values('id')))

            playlistsongs = PlaylistSong.objects.filter(playlist=alarm.playlist).values('song')
            """ query clause = select song from playlistsong where playlist = playlist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(playlistsongs))


        elif alarm.artist: #if only the artist available

            songs = Song.objects.filter(artist = alarm.artist)
            """ clause query = select * from song where artist = artist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(songs.values('id')))

        elif alarm.playlist: #if only the playlist available

            songs = PlaylistSong.objects.filter(playlist = alarm.playlist)
            """ query clause = select song from playlistsong where playlist = playlist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(songs.values('song')))
        else:
            logger.debug("this alarm has no playlist nor artist")

        """ after creating the list I will remove the duplicate, shuffle the songs and limit themto the total_songs """

        final_list = list(set(songs_list)) #converting the list to a set and back to list (to remove duplicates)

        random.shuffle(final_list) #reshuffle the songs randomly


        return final_list[0:total_songs]