from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
import logging
from .models import Artist, Song, Playlist, PlaylistSong
from .forms import UserForm, LoginForm


logger = logging.getLogger('library')
@login_required
def index(request):
    logger.debug("index request, request :%s", request)
    return render(request=request, template_name='library/index.html' ,context={})

@login_required
def artists(request):
    logger.debug("list of all artists")
    artistlist = Artist.objects.all()
    context = {
        'artistlist' : artistlist,
    }
    return render(request=request, template_name='library/artists.html' ,context=context)

@login_required
def artist_details(request,pk):
    logger.debug("Artist details, request: %s, artist_id: %s", request, pk)

    artist = get_object_or_404(Artist, pk=pk)
    logger.debug("artist details found :%s", artist)

    return render(request=request, template_name='library/artist_details.html', context={'artist' : artist})



class ArtistCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    logger.debug("artist add")
    permission_required = 'library.add_artist'
    model = Artist
    fields = ['name', 'nationality','image']

class ArtistUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    logger.debug("artist update")
    permission_required = 'library.edit_artist'
    model = Artist
    fields = ['name', 'nationality','image']


class ArtistDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    logger.debug("artist delete")
    permission_required = 'library.delete_artist'
    model = Artist
    success_url = reverse_lazy('library:artists')


# songs section
@login_required
def songs(request):
    logger.debug("songs list request")
    songlist = Song.objects.all()
    return render(request=request, template_name='library/songs.html', context={'songlist':songlist})

@login_required
def song_details(request, pk):
    logger.debug("request : %s, song_id : %s", request, pk)
    song = get_object_or_404(Song, pk=pk)
    return render(request=request, template_name='library/song_details.html', context={'song': song,'hour_len':len(str(song.duration.hour))})



class SongCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    logger.debug("song add")
    permission_required = 'library.add_song'
    model = Song
    fields = ['name','year','duration','artist', 'enabled', 'file']

class SongUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    logger.debug("song update")
    permission_required = 'library.change_song'
    model = Song
    fields = ['name','year','duration','artist',  'enabled', 'file']

class SongDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    logger.debug("song delete")
    permission_required = 'library.delete_song'
    model = Song
    success_url = reverse_lazy('library:songs')


def song_enable(request):
    song_id = request.POST['song_id']
    logger.debug("request : %s and song_id : %s", request.POST, song_id)
    song = Song.objects.get(pk=song_id)
    song.enabled = False
    song.save()
    return render(request=request, template_name='library/song_details.html',
                  context={'song': song, 'hour_len': len(str(song.duration.hour))})


#playlist section
class PlaylistList(LoginRequiredMixin,generic.ListView):
    template_name = 'library/playlists.html'
    context_object_name = 'playlists'

    logger.debug("playlist request")
    def get_queryset(self):
        pls = Playlist.objects.all()
        logger.debug("pls :%s", pls)
        return pls

@login_required
def playlist_details(request,pk):
    logger.debug("Playlist details, request: %s, playlist_id: %s", request, pk)

    playlist = get_object_or_404(Playlist, pk=pk)
    logger.debug("playlist details found :%s", playlist)

    return render(request=request, template_name='library/playlist_details.html', context={'playlist' : playlist})


class PlaylistCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    logger.debug("create playlist view")
    permission_required = 'library.add_playlist'
    model = Playlist
    fields = ['name']

class PlaylistUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    logger.debug("update playlist view")
    permission_required = 'library.change_playlist'
    model = Playlist
    fields = ['id','name']

class PlaylistDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    logger.debug("playlist delete")
    permission_required = 'library.delete_playlist'
    model = Playlist
    success_url = reverse_lazy('library:playlists')
#    context_object_name = 'playlist'

#playlistsong section
class PlsList(LoginRequiredMixin,generic.ListView):
    template_name = 'library/playlist_songs.html'
    context_object_name = 'playlistsongs'
    logger.debug('playlistsong request')

    def get_queryset(self):
        pls = PlaylistSong.objects.all()
        logger.debug("pls : %s", pls)
        return pls

@login_required
def pls_details(request,pk):
    logger.debug("Pls details, request: %s, pls_id: %s", request, pk)

    pls = get_object_or_404(PlaylistSong, pk=pk)
    logger.debug("pls details found :%s", pls)

    return render(request=request, template_name='library/playlist_song_details.html', context={'pls' : pls})

class PlsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    logger.debug("create playlist view")
    permission_required = 'library.add_playlistsong'
    model = PlaylistSong
    fields = ['playlist','song','active']


class PlsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    logger.debug("update playlist view")
    permission_required = 'library.change_playlist'
    model = PlaylistSong
    fields = ['playlist', 'song', 'active']


class PlsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    logger.debug("playlist delete")
    permission_required = 'library.delete_playlist'
    model = PlaylistSong
    success_url = reverse_lazy('library:pls')


class UserFormView(View):

    form_class = UserForm
    template_name = 'library/registration_form.html'
    logger.debug("userform")

    def get(self, request):
        logger.debug("request from get : %s", request)
        form = self.form_class(None)
        return render(request=request, template_name=self.template_name, context={'form':form})


    def post(self, request):
        form = self.form_class(request.POST)
        logger.debug("request from post : %s", request)

        if form.is_valid():

            logger.debug("form is valid")

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logger.debug("username & password before set %s , %s", username, password)
            user.set_password(password)
            logger.debug("password after set : %s", password)
            user.save()

            logger.debug("user saved")

            user = authenticate(username=username, password=password)
            logger.debug("user authenticate : %s", user)

            if user is not None:
                logger.debug("user is not None")
                if user.is_active:
                    logger.debug("user is active")
                    login(request=request, user=user)
                    logger.debug("login userand redirect")
                    return redirect('library:home')

        logger.error("an error during authentication")
        return render(request=request, template_name=self.template_name, context={'form': form})

class LogingFormView(View):

    form_class = LoginForm
    template_name = 'library/registration_form.html'
    logger.debug("login form")

    def get(self,request):
        logger.debug("login get request : %s", request)
        form = self.form_class(None)
        return render(request=request, template_name=self.template_name, context={'form': form})

    def post(self,request):
        logger.debug("post request : %s", request.POST)
        form = self.form_class(request.POST)

#        if form.is_valid():

        logger.debug("form is valid : %s", request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.debug("username & password before set %s , %s", username, password)

        user = authenticate(username=username, password=password)
        logger.debug("user authenticate : %s", user)

        if user is not None:
            logger.debug("user is not None")
            if user.is_active:
                logger.debug("user is active")
                login(request=request, user=user)
                logger.debug("login user and redirect")
                return redirect('library:home')

        else:
            logger.error("an error during authentication")
            return render(request=request, template_name=self.template_name, context={'form': form})

def logout_user(request):
    logger.debug("logout user")
    template_name = 'library/index.html'
    logout(request=request)
    return render(request=request, template_name=template_name,context={'user':'loggedout'})