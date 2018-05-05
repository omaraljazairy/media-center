from django.test import TestCase
from alarmclock.scheduler import Scheduler
from alarmclock.models import Alarms
from library.models import Artist, Song, Playlist, PlaylistSong
from datetime import datetime

class SchedulerTest(TestCase):
	''' test for all the methods in the Scheduler class '''

	def setUp(self):
		''' create songs, artists, playlists and alarms '''

		day = {
		'Saturday'	: 0,
		'Sunday'	: 1,
		'Monday'	: 2,
		'Tuesday'	: 3,
		'Wednesday'	: 4,
		'Thursday'	: 5,
		'Friday'	: 6,
		}

		current_dayname = datetime.today().strftime("%A")
		# playlist
		pl_1 = Playlist.objects.create(name='my_playlist1')
		pl_2 = Playlist.objects.create(name='my_playlist2')
		
		# artist
		roger = Artist.objects.create(name='Roger', nationality='Swiss')
		
		# songs
		my_song1 = Song.objects.create(name='hello1',year='2018-01-01',duration='01:01:00',artist=roger,source='file')
		my_song2 = Song.objects.create(name='hello2',year='2017-01-01',duration='03:01:00',artist=roger,source='file')
		my_song3 = Song.objects.create(name='hello3',year='2016-01-01',duration='02:01:00',artist=roger,source='file')

		# plalistsongs
		PlaylistSong.objects.create(playlist=pl_1, song=my_song1)
		PlaylistSong.objects.create(playlist=pl_1, song=my_song2)
		PlaylistSong.objects.create(playlist=pl_2, song=my_song3)
		
		# alarmclock
		Alarms.objects.create(name='my_alarm1',daily=True,hour='11:00:00', playlist=pl_1, total_songs=1, active=True)
		Alarms.objects.create(name='my_alarm2', daily=True,hour='12:00:00', playlist=pl_2, total_songs=1, active=True)
		#Alarms.objects.create(name='my_alarm4', daily=True,hour='10:00:00', artist=roger, total_songs=1, active=True)
		Alarms.objects.create(name='my_alarm3',day=Alarms.DAY_CHOICES[day[current_dayname]],daily=False,hour='09:00:00',artist=roger, playlist=pl_1, total_songs=2, active=True)

		self.scheduler = Scheduler()

	def test_date(self):
		''' test if the date returned is correct '''

		current_dayname = datetime.today().strftime("%A")
		current_date	= datetime.now().strftime('%Y-%m-%d')

		scheduler_date = self.scheduler.get_date_day()
		
		self.assertEquals(scheduler_date['day'],current_dayname)
		self.assertEquals(scheduler_date['date'],current_date)

	def test_get_scheduled_alarms(self):
		''' check if we get the correct number of available alarms from the get_available_alarms '''

		total = self.scheduler.get_scheduled_alarms()
		self.assertEqual(len(total),3)
		self.assertEquals(type(total),list)


	def test_alarm_details(self):
		''' check if the details are correct as expected '''

		alarms = self.scheduler.get_scheduled_alarms()
		alarm_details = self.scheduler.get_alarm_details(alarms)

		self.assertEquals(type(alarm_details),list)
		self.assertEquals(type(alarm_details[0]),dict)
		self.assertIsInstance(alarm_details[0]['id'],Alarms)


	def test_songs_from_alarms(self):
		''' trst if we get the correct nuber of songs '''

		alarms = self.scheduler.get_scheduled_alarms()
		alarm_details = self.scheduler.get_alarm_details(alarms)
		alarm1 = alarm_details[0]['id']
		alarm2 = alarm_details[1]['id']
		#alarm3 = alarm_details[2]['id']

		alarm_song_list1 = self.scheduler.get_songs_from_alarm(alarm1, total_songs=1)
		alarm_song_list2 = self.scheduler.get_songs_from_alarm(alarm2, total_songs=1)
		#alarm_song_list3 = self.scheduler.get_songs_from_alarm(alarm3, total_songs=2)

		self.assertEqual(len(alarm_song_list1),1)
		self.assertEqual(len(alarm_song_list2),1)
		#self.assertEqual(len(alarm_song_list3),2)
