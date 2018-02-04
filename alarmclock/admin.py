from django.contrib import admin
from .models import PlayedSongs, Alarms, QueuedSongs
# Register your models here.

class PlayedSongsAdmin(admin.ModelAdmin):

    list_display = ['alarm','song', 'played']
    list_per_page = 20
    ordering = ('-played',)

class AlarmsAdmin(admin.ModelAdmin):

    list_display = ('name','created','hour','artist','playlist','total_songs','active',)
#    list_display = ('day',)


class QueuedSongsAdmin(admin.ModelAdmin):

    list_display = ['alarm','scheduled','played']


admin.site.register(PlayedSongs, admin_class=PlayedSongsAdmin)
admin.site.register(Alarms, admin_class=AlarmsAdmin)
admin.site.register(QueuedSongs, admin_class=QueuedSongsAdmin)