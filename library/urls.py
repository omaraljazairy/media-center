from django.conf.urls import url
from . import views

app_name = 'library'

urlpatterns = [
    url(r'^$',views.index, name='home'),
#    url(r'register/$',views.UserFormView.as_view(), name='register'),
#    url(r'login/$',views.LogingFormView.as_view(), name='login'),
#    url(r'logout/$', views.logout_user, name='logout'),
    # artist section urls
    url(r'artists/$',views.artists, name='artists'),
    url(r'artistdetails/(?P<pk>[0-9]+)/$',views.artist_details,name="artist_details"),
    url(r'artist/add/$', views.ArtistCreate.as_view(), name='artist_add'),
    url(r'artist/edit/(?P<pk>[0-9]+)/$', views.ArtistUpdate.as_view(), name='artist_edit'),
    url(r'artist/delete/(?P<pk>[0-9]+)/$', views.ArtistDelete.as_view(), name='artist_delete'),

    # songs section urls
    url(r'songs/$', views.songs, name='songs'),
    url(r'songdetails/(?P<pk>[0-9]+)/$', views.song_details, name="song_details"),
    url(r'songenable/$', views.song_enable, name="song_enable"),
    url(r'song/add/$', views.SongCreate.as_view(), name='song_add'),
    url(r'song/edit/(?P<pk>[0-9]+)/$', views.SongUpdate.as_view(), name='song_edit'),
    url(r'song/delete/(?P<pk>[0-9]+)/$', views.SongDelete.as_view(), name='song_delete'),

    # playlist section urls
    url(r'playlists/$', views.PlaylistList.as_view(), name='playlists'),
    url(r'playlistdetails/(?P<pk>[0-9]+)/$', views.playlist_details, name="playlist_details"),
    url(r'playlist/add/$', views.PlaylistCreate.as_view(), name='playlist_add'),
    url(r'playlist/edit/(?P<pk>[0-9]+)/$', views.PlaylistUpdate.as_view(), name='playlist_edit'),
    url(r'playlist/delete/(?P<pk>[0-9]+)/$', views.PlaylistDelete.as_view(), name='playlist_delete'),

    #playistsong section
    url(r'pls/$', views.PlsList.as_view(), name='pls'),
    url(r'plsdetails/(?P<pk>[0-9]+)/$', views.pls_details, name="playlistsong_details"),
    url(r'pls/add/$', views.PlsCreate.as_view(), name='playlistsong_add'),
    url(r'pls/edit/(?P<pk>[0-9]+)/$', views.PlsUpdate.as_view(), name='playlistsong_edit'),
    url(r'pls/delete/(?P<pk>[0-9]+)/$', views.PlsDelete.as_view(), name='playlistsong_delete'),
]