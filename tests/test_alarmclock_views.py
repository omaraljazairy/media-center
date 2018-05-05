from alarmclock.models import Alarms
from library.models import Artist, Playlist
from django.test import TestCase


class AlarmViewTest(TestCase):
	''' tests for the alarm view '''

	def setUp(self):
		''' create the alarms '''

		pl = Playlist.objects.create(name='my_playlist')
		roger = Artist.objects.create(name='Roger', nationality='Swiss')

		total_alarms = 3
		for i in range(total_alarms):
			hour = '1'.__add__(str(i)).__add__(':00:00')
			Alarms.objects.create(name='my_alarm_%s' % i, day=Alarms.DAY_CHOICES[0] ,daily=False, hour=hour, artist=roger, playlist=pl, total_songs=5, active=True)



	def test_success_view(self):
		''' check if we get response 200 when viewing the alarms list '''
		
		resp = self.client.get('/alarmclock/alarms/')
		self.assertEqual(resp.status_code,200)


	def test_success_view_details(self):
		''' check if we get response 200 when viewing the alarms list '''
		
		resp = self.client.get('/alarmclock/alarm/details/2/')
		self.assertEqual(resp.status_code,200)


	def test_error_view_details(self):
		''' check if we get response 200 when viewing the alarms list '''
		
		resp = self.client.get('/alarmclock/alarm/details/7/')
		self.assertEqual(resp.status_code,404)
