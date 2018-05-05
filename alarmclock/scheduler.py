from datetime import datetime
from django.utils import timezone
from .models import Alarms
from library.models import PlaylistSong, Song
from mediacenter.utils import QuerySetConverter
import logging
import random

logger = logging.getLogger('scheduler')


class Scheduler():
    ''' this class schedules the alarms set in the Alarms model
        it will do the following:
        1- read check the scheduled alarms per day (daily / currentday).
        2- creates a list of the songs from the artist and playlists set
         by the alarm.
        3- it will schedule the songs based on hour set in the alarm.
        4- the scheduled alarms will be saved in the queuedsongs table.
    '''

    available_alarms = None

    def __init__(self):
        ''' the scheduler init will check first if there are any scheduled alarms available for today '''
        logger.debug("scheduler started")
        self.date_day = self.get_date_day()

    def get_date_day(self):
        """ setting the current day name and date and returning them in a dict """
        now = timezone.now()
        today_day = now.strftime("%A")
        today_date = timezone.now().strftime('%Y-%m-%d')
        logger.debug("today's day is : %s and date: %s", today_day, today_date)
        return {'day': today_day, 'date': today_date}

    def get_scheduled_alarms(self):
        """ this function searches for the available scheduled alarms and returns the alarm objects in a list"""

        ''' create a list of the alarm which are not currently in the queued_songs table '''

        alarm = Alarms.objects.get_queryset().available_alarms(self.date_day)

        return list(alarm)


    def get_alarm_details(self,alarm):
        """ get the alarm object which contains all the available scheduled alarms for currentday """

        alarm_details = [] #list to save all the song_ids

        for i in range(0,len(alarm)): #looping through the alarms


            alarm_datetime_string = self.date_day['date'] +" ".__add__(str(alarm[i].hour))
            alarm_datetime = datetime.strptime(alarm_datetime_string,'%Y-%m-%d %H:%M:%S')

            total = int(alarm[i].total_songs) #total songs
            songs = self.get_songs_from_alarm(alarm[i], total_songs=total)


            data = {
                'id':alarm[i], # Alarms.objects.get(pk=alarm[i].id),
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
            #songs = Song.objects.filter(artist = alarm.artist)
            songs = Song.objects.get_queryset().valid_songs().by_artist(alarm.artist)
            """ query clause = select * from song where artist = artist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(songs.values('id')))

            playlistsongs = PlaylistSong.objects.filter(playlist=alarm.playlist,song__enabled= True).values('song')
            """ query clause = select song from playlistsong where playlist = playlist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(playlistsongs))


        elif alarm.artist: #if only the artist available

            #songs = Song.objects.filter(artist = alarm.artist, enabled= True)
            songs = Song.objects.get_queryset().valid_songs().by_artist(alarm.artist)
            """ clause query = select * from song where artist = artist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(songs.values('id')))

        elif alarm.playlist: #if only the playlist available

            songs = PlaylistSong.objects.filter(playlist = alarm.playlist,song__enabled= True)
            """ query clause = select song from playlistsong where playlist = playlist """

            """ converts the queryset to a list and add the songids in the song_list list """
            songs_list.extend(QuerySetConverter().to_list(songs.values('song')))
        else:
            logger.debug("this alarm has no playlist nor artist")

        """ after creating the list I will remove the duplicate, shuffle the songs and limit themto the total_songs """

        final_list = list(set(songs_list)) #converting the list to a set and back to list (to remove duplicates)

        random.shuffle(final_list) #reshuffle the songs randomly


        return final_list[0:total_songs]
