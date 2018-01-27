from django.contrib import admin
from library.models import Artist, Song, Playlist, PlaylistSong, PlayedSongs
# Register your models here.

class ArtistAdmin(admin.ModelAdmin):

    list_display = ['id','name', 'nationality', 'created','image']

class SongAdmin(admin.ModelAdmin):

    list_display = ['id', 'name','year','duration','artist', 'created', 'enabled', 'file']

class PlaylistAdmin(admin.ModelAdmin):

    list_display = ['id', 'name','created']

class PlaylistSongAdmin(admin.ModelAdmin):

    list_display = ['id','playlist','song','added','active']

class PlayedSongsAdmin(admin.ModelAdmin):

    list_display = ['song', 'played']


admin.site.register(Artist, admin_class=ArtistAdmin)
admin.site.register(Song, admin_class=SongAdmin)
admin.site.register(Playlist,admin_class=PlaylistAdmin)
admin.site.register(PlaylistSong,admin_class=PlaylistSongAdmin)
admin.site.register(PlayedSongs, admin_class=PlayedSongsAdmin)
