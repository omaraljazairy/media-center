from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from .utils import Choices

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

    class Meta:
        ordering = ('added',)
        get_latest_by = "added"
        unique_together = ('playlist','song')
        verbose_name_plural = "PlaylistSong"

    def get_absolute_url(self):
        return reverse('library:playlistsong_details',kwargs={'pk':self.pk})


    def __str__(self):
        return self.playlist.name + ' ' + self.song.name


class PlayedSongs(models.Model):

    song        = models.ForeignKey(
        Song,
        related_name='played_song',
        on_delete=models.CASCADE
    )
    played      = models.DateTimeField(verbose_name="Song played time", db_index=True)


    class Meta:
        ordering = ('played',)
        verbose_name_plural = "PlayedSongs"

    def __str__(self):
        return str(self.played)

