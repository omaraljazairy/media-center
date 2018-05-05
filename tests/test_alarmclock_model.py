from django.test import TestCase
from alarmclock.models import Alarms, QueuedSongs, PlayedSongs
from library.models import Artist, Playlist, Song
from django.db.utils import IntegrityError
from datetime import datetime


class AlarmTest(TestCase):
	""" testing the Alarm class """

	@classmethod
	def setUpTestData(cls):
		''' setup the alarm object '''

		pl = Playlist.objects.create(name='my_playlist')
		roger = Artist.objects.create(name='Roger', nationality='Swiss')

		Alarms.objects.create(name='my_alarm',day=Alarms.DAY_CHOICES[0],daily=False,hour='10:00:00',artist=roger, playlist=pl, total_songs=5, active=True)


	def test_created_alarm(self):
		''' testing the creation of the Alarm '''

		a = Alarms.objects.get(id=1)
		self.assertTrue(isinstance(a , Alarms) )


	def test_duplicate_alarms(self):
		''' check if two alarms created with same name will throw an exception '''
	
		pl = Playlist.objects.create(name='my_playlist2')
		roger = Artist.objects.create(name='Roger2', nationality='Swiss')

		with self.assertRaises(IntegrityError):

			Alarms.objects.create(name='my_alarm',day=Alarms.DAY_CHOICES[0],daily=False,hour='10:00:00',artist=roger, playlist=pl, total_songs=5, active=True)


	def test_default_executed_value(self):
		''' test if the default value of the created alarm is set to 2018-01-01 00:00:00 '''

		alarm = Alarms.objects.get(pk=1)
		self.assertEquals(alarm.executed.strftime('%Y-%m-%d %H:%M:%S'), '2018-01-01 00:00:00')


	def test_verbose_plural(self):
		''' check the plural name from the meta class '''

		alarm = Alarms.objects.get(pk=1)
		self.assertEqual(str(alarm._meta.verbose_name_plural), 'Alarms', msg=None)


	def test_repr(self):
		''' test the __str__ returned from the object '''

		alarm = Alarms.objects.get(pk=1)
		self.assertEqual(str(alarm),alarm.name)

	def test_get_absolute_url(self):
		''' get the absolute url '''
		
		alarm = Alarms.objects.get(id=1)
		self.assertEquals(alarm.get_absolute_url(),'/alarmclock/alarm/details/1/')


	def test_available_alarms(self):
		''' test the manager and queryset '''

		date = {'day': 'Saturday'}
		alarm = Alarms.objects.get_queryset().available_alarms(date)
		self.assertTrue(alarm)

class QueuedSongsTest(TestCase):
	''' tests for the QueuedSongs model '''

	
	def setUp(self):
		''' creating the alarm and the song needed for the creation of this model '''

		pl = Playlist.objects.create(name='my_playlist')
		roger = Artist.objects.create(name='Roger', nationality='Swiss')
		alarm = Alarms.objects.create(name='my_alarm',day=Alarms.DAY_CHOICES[0],daily=False,hour='10:00:00',artist=roger, playlist=pl, total_songs=5, active=True)
		song = Song.objects.create(name='hello',year='2018-01-01',duration='01:01:00',artist=roger,source='file')
		QueuedSongs.objects.create(alarm=alarm, song=song, scheduled=datetime.now())


	def test_created_queuedsong(self):
		''' test the creation of the queuedsong '''

		qs = QueuedSongs.objects.get(id=1)
		self.assertTrue(isinstance(qs,QueuedSongs))


	def test_queued_songs(self):
		''' check if we get a song in the queue '''

		qs = QueuedSongs.objects.get_queryset().get_current_queued_alarms()
		self.assertTrue(qs)

	def test_repr(self):
		''' test that we get back the scheduled time of the song/alarm '''

		qs = QueuedSongs.objects.get(id=1)
		self.assertEqual(str(qs), qs.scheduled.strftime('%Y-%m-%d %H:%M:%S'))


class PlayedSongsTest(TestCase):
	''' tests for the PlayedSongs model '''

	def setUp(self):
		''' setting up the models needed for the PlayedSong model '''
		pl = Playlist.objects.create(name='my_playlist')
		roger = Artist.objects.create(name='Roger', nationality='Swiss')
		alarm = Alarms.objects.create(name='my_alarm',day=Alarms.DAY_CHOICES[0],daily=False,hour='10:00:00',artist=roger, playlist=pl, total_songs=5, active=True)
		song = Song.objects.create(name='hello',year='2018-01-01',duration='01:01:00',artist=roger,source='file')
		PlayedSongs.objects.create(alarm=alarm, song=song, played=datetime.today())


	def test_created_playedsongs(self):
		''' test if thr playedsongs objectis created '''

		ps = PlayedSongs.objects.get(id=1)
		self.assertTrue(isinstance(ps, PlayedSongs))



	def test_manager(self):
		''' test if the manager gives back the played song of today '''

		today_song = PlayedSongs.objects.get_todays_played_alarms()
		self.assertTrue(today_song)

	def test_played_repr(self):
		''' check the played song '''

		ps = PlayedSongs.objects.get(id=1)
		self.assertEqual(ps.played.strftime('%Y-%m-%d %H:%M:%S'), datetime.today().strftime('%Y-%m-%d %H:%M:%S'))




