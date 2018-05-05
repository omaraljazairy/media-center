from django.test import TestCase
from library.models import Artist, Song, Playlist, PlaylistSong
from django.db.utils import IntegrityError

# Create your tests here.
class ArtistModelTest(TestCase):


	def setUp(self):
		''' setting up two Artist objects '''

		self.roger = Artist.objects.create(name='Roger', nationality='Swiss')
		self.rafa = Artist.objects.create(name='Rafa', nationality='Swiss')
		print("setup artist")

	def test_creation_artist(self):
		''' test that we get the Artist object after create with on the name and nationality '''

		print("setup artist")
		artist = Artist.objects.get(name='Roger')
		self.assertTrue(isinstance(artist, Artist))
	

	def test_returned_repr(self):
		''' testing that the __str__ is always the name of the artist . '''
		
		artist = Artist.objects.get(name='Roger')
		self.assertEqual(str(artist), artist.name)

	def test_default_image(self):
		''' the default value of the image if it's not provided should be no-image.gif '''

		artist = Artist.objects.get(name='Roger')
		self.assertEqual(str(artist.image), 'no-image.gif')


	def test_verbose_plural(self):
		''' check the plural name from the meta class '''

		artist = Artist.objects.get(name='Roger')
		self.assertEqual(str(artist._meta.verbose_name_plural), 'Artist', msg=None)

	def test_name(self):
		''' testing the name is correctly stored and fetched '''

		artist = Artist.objects.get(name='Roger')
		self.assertEqual(artist.name, 'Roger')


	def test_name_max_length(self):
		''' test the length of the name column '''

		artist = Artist.objects.get(name='Roger')
		max_length = artist._meta.get_field('name').max_length
		self.assertEquals(max_length,50)


	def test_get_absolute_url(self):
		''' get the absolute url '''
		
		artist = Artist.objects.get(id=1)
		self.assertEquals(artist.get_absolute_url(),'/mediacenter/artistdetails/1/')


	def tearDown(self):
		''' removing the object '''

		self.roger.delete()
		self.rafa.delete()

class SongModelTest(TestCase):
	''' testing the Song class together with the SongManager and SongQuerySet '''

	hello = None

	def setUp(self):
		''' setting up one Song models objects '''

		self.roger = Artist.objects.create(name='Roger', nationality='Swiss')
		Song.objects.create(name='hello2',year='2018-01-01',duration='01:01:00',artist=self.roger,source='file')
		print("setup")
		

	def test_create_song(self):
		''' testing the creation of the Song object '''

		song = Song.objects.get(name='hello2')
		
		self.assertTrue(isinstance(song, Song))

	def test_repr(self):
		''' check that the __str__ is the song name ''' 

		song = Song.objects.get(name='hello2')
		self.assertEqual(str(song), song.name)
#		self.assertEqual(int(song.favorite),1)

	def test_favorite(self):
		''' check that the __str__ is the song name ''' 
		
		song = Song.objects.get(name='hello2')
		self.assertEqual(int(song.favorite),1)



	def test_unique_songs(self):
		''' testing the uniqueness of duplicate songs '''


		with self.assertRaises(IntegrityError):
			Song.objects.create(name='hello2',year='2018-01-01',duration='01:01:00',artist=self.roger,source='file')
		

	def test_manager_invalid_song(self):
		''' testing the SongManager and QuerySet that should give an empty list'''

		qs = Song.objects.get_queryset().valid_songs()

		self.assertQuerysetEqual(qs,[])

	def test_manager_with_artist(self):
		''' testing the SongManager and QuerySet that should a song belongs to the artist'''
		
		qs = Song.objects.get_queryset().by_artist(self.roger)
		
	
		self.assertTrue(qs)


class PlaylistTest(TestCase):
	''' testing the Playlist model class '''

	@classmethod
	def setUpTestData(cls):
		''' setting up the playlist model class '''

		Playlist.objects.create(name='my_playlist')


	def test_str(self):
		''' testing the str representation '''

		#pl = Playlist.objects.create(name='my_playlist')
		pl = Playlist.objects.get(id=1)
		self.assertTrue(isinstance(pl, Playlist))


	def test_verbose_plural(self):
		''' test if the plural is returned '''

		pl = Playlist.objects.get(name='my_playlist')
		self.assertEqual(str(pl._meta.verbose_name_plural),'Playlist')





class PlaylistSongTest(TestCase):
	''' tests for the PlaylistSong model class '''

	def setUp(self):

		self.pl = Playlist.objects.create(name='my_playlist')
		self.roger = Artist.objects.create(name='Roger', nationality='Swiss')
		self.song = Song.objects.create(name='hele',year='2018-01-01',duration='01:01:00',artist=self.roger,source='file')

		PlaylistSong.objects.create(playlist=self.pl, song=self.song,active=False)

	def test_created_playlistsong(self):
		''' testing the creation of the object '''

		pls = PlaylistSong.objects.get(pk=1)
		self.assertTrue(isinstance(pls, PlaylistSong))


	def test_repr(self):
		''' testing the representation when calling the model '''

		pls = PlaylistSong.objects.get(pk=1)
		self.assertEqual(str(pls),'my_playlist hele')


	
	def test_unique_playlistsong(self):
		''' testing the meta uniqueness '''
	
		#pl = Playlist.objects.create(name='my_playlist')
		#roger = Artist.objects.create(name='Roger', nationality='Swiss')
		#song = Song.objects.create(name='hele',year='2018-01-01',duration='01:01:00',artist=roger,source='file')

		with self.assertRaises(IntegrityError):
			PlaylistSong.objects.create(playlist=self.pl, song=self.song,active=True)

	