from django.test import TestCase
from library.models import Artist, Song, Playlist, PlaylistSong
from django.contrib.auth.models import User

class ArtistListViewTest(TestCase):
	''' tests of the views '''

	def setUp(self):

		#creating the user
		user1 = User.objects.create_user(username="test1", password="12345")
		user1.save()

		#creating the artists
		nr_artist = 5
		for i in range(nr_artist):
			Artist.objects.create(name='Roger %s' % i, nationality='Iraqi')



	def test_view_redirect_not_logged_in(self):
		''' test if the not logged in user gets redirected to the login page '''

		resp = self.client.get('/mediacenter/artists/')
		self.assertRedirects(resp, '/accounts/login/?next=/mediacenter/artists/')


	def test_view_redirect_logged_in(self):
		''' test that the logged in user goes to the artist page with statuscode 200 without being redirected to the login page '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/artists/')
		self.assertEqual(resp.status_code,200)

	def test_if_user_is_user(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/artists/')
		self.assertEqual(str(resp.context['user']),'test1')


	def test_if_template_used(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/artists/')
		self.assertTemplateUsed(resp, 'library/artists.html')


class SongViewTest(TestCase):
	''' view tests for the song view '''

	def setUp(self):
		''' setting up the user, artist and song '''

		#creating the user
		user1 = User.objects.create_user(username="test1", password="12345")
		user1.save()

		#creating the artists
		artist = Artist.objects.create(name='Roger', nationality='Iraqi')
		nr_songs = 5
		for i in range(nr_songs):
			Song.objects.create(name='hello %s' % i, year='2018-01-01', duration='01:01:00', artist=artist, source='file')

	def test_view_redirect_not_logged_in(self):
		''' test if the not logged in user gets redirected to the login page '''

		resp = self.client.get('/mediacenter/songs/')
		self.assertRedirects(resp, '/accounts/login/?next=/mediacenter/songs/')


	def test_view_redirect_logged_in(self):
		''' test that the logged in user goes to the songs page with statuscode 200 without being redirected to the login page '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/songs/')
		self.assertEqual(resp.status_code,200)

	def test_if_user_is_user(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/songs/')
		self.assertEqual(str(resp.context['user']),'test1')


	def test_if_template_used(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/songs/')
		self.assertTemplateUsed(resp, 'library/songs.html')


class PlaylistViewTest(TestCase):
	''' playlist views tests '''

	def setUp(self):

		#creating the user
		user1 = User.objects.create_user(username="test1", password="12345")
		user1.save()

		#creating the playlists
		nr_playlist = 5
		for i in range(nr_playlist):
			Playlist.objects.create(name="playlist %s" % i)

	def test_view_redirect_not_logged_in(self):
		''' test if the not logged in user gets redirected to the login page '''

		resp = self.client.get('/mediacenter/playlists/')
		self.assertRedirects(resp, '/accounts/login/?next=/mediacenter/playlists/')


	def test_view_redirect_logged_in(self):
		''' test that the logged in user goes to the songs page with statuscode 200 without being redirected to the login page '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/playlists/')
		self.assertEqual(resp.status_code,200)

	def test_if_user_is_user(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/playlists/')
		self.assertEqual(str(resp.context['user']),'test1')


	def test_if_template_used(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/playlists/')
		self.assertTemplateUsed(resp, 'library/playlists.html')



class PlaylistSongViewTet(TestCase):
	''' playlistsong views test '''

	def setUp(self):

		#creating the user
		user1 = User.objects.create_user(username="test1", password="12345")
		user1.save()

		#creating the playlists
		artist = Artist.objects.create(name='Roger', nationality='Iraqi')
		song = Song.objects.create(name='hello', year='2018-01-01', duration='01:01:00', artist=artist, source='file')
		playlist = Playlist.objects.create(name="playlist")

		PlaylistSong.objects.create(playlist=playlist, song=song)


	def test_view_redirect_not_logged_in(self):
		''' test if the not logged in user gets redirected to the login page '''

		resp = self.client.get('/mediacenter/pls/')
		self.assertRedirects(resp, '/accounts/login/?next=/mediacenter/pls/')


	def test_view_redirect_logged_in(self):
		''' test that the logged in user goes to the songs page with statuscode 200 without being redirected to the login page '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/pls/')
		self.assertEqual(resp.status_code,200)

	def test_if_user_is_user(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/pls/')
		self.assertEqual(str(resp.context['user']),'test1')


	def test_if_template_used(self):
		''' check if the username is the correct user name in the response context '''

		self.client.login(username='test1', password='12345')
		resp = self.client.get('/mediacenter/pls/')
		self.assertTemplateUsed(resp, 'library/playlist_songs.html')
