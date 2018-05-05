from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from mediacenter.utils import Choices


class Artist(models.Model):

    name        = models.CharField(max_length=50, unique=True, blank=False, null=False)
    nationality =   models.CharField(max_length=30, )
    created     = models.DateTimeField(auto_now_add=True, db_index=True)
    image       = models.FileField(upload_to='images/' , null=True, blank=True,default='no-image.gif')

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Artist"


    def get_absolute_url(self):
        return reverse('library:artist_details',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class SongQuerySet(models.query.QuerySet):
    ''' this queryset returns only active and valid songs '''
    
    def valid_songs(self):
        ''' returns a song which is enabled and has no "no-file" ''' 
        
        return self.filter(enabled= True).exclude(file__contains= 'no-file')


    def by_artist(self, artist):
        ''' returns the song by the artist arg '''

        return self.filter(artist = artist)


class SongManager(models.Manager):
    ''' gets the queryset to give back a valid song '''

    def get_queryset(self):
        ''' gets the queryset method from the QuerySet class ''' 
        return SongQuerySet(self.model, using=self._db)


class Song(models.Model):

    class MediaSource(Choices):
        FILE    = 'file'
        YOUTUBE = 'youtube'

    name    = models.CharField(max_length=50,blank=False,null=False, db_index=True)
    year    = models.DateField(null=True,db_index=True)
    duration  = models.TimeField(verbose_name="the length of the song", db_index=True)
    artist  = models.ForeignKey(
        Artist,
        related_name='songs',
        on_delete=models.CASCADE
    )
    source = models.CharField(max_length=7, choices=MediaSource.choices(), null=False)
    created = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True, db_index=True)
    favorite = models.IntegerField(db_index=True, default=1)
    file = models.FileField(upload_to='songs/', null=True, default='no-file')
    objects = SongManager()

    class Meta:
        ordering = ('id',)
        unique_together = ('name','artist')
        verbose_name_plural = "Song"

    def get_absolute_url(self):
        return reverse('library:song_details',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class Playlist(models.Model):

    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Playlist"


    def get_absolute_url(self):
        return reverse('library:playlist_details',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name


class PlaylistSongQuerySet(models.query.QuerySet):
    ''' this queryset returns only active and valid songs '''
    
    def valid_songs(self):
        ''' returns a song which is enabled and has no "no-file" ''' 
        return self.filter(song__enabled= True).exclude(song__file__contains= 'no-file')

class PlaylistSongManager(models.Manager):
    ''' gets the queryset to give back a valid song '''

    def get_queryset(self):
        ''' gets the queryset method from the QuerySet class ''' 
        return PlaylistSongQuerySet(self.model, using=self._db)



class PlaylistSong(models.Model):

    playlist = models.ForeignKey(
        Playlist,
        related_name='playlist',
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        Song,
        related_name='song',
        on_delete=models.CASCADE
    )

    added = models.DateTimeField(auto_now=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
#    pl_valid_song = PlaylistSongManager()


    class Meta:
        ordering = ('added',)
        get_latest_by = "added"
        unique_together = ('playlist','song')
        verbose_name_plural = "PlaylistSong"

    def get_absolute_url(self):
        return reverse('library:playlistsong_details',kwargs={'pk':self.pk})


    def __str__(self):
        return self.playlist.name + ' ' + self.song.name
