from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Alarms
from django.urls import reverse_lazy
import logging
from .tasks import check_queue, play_queued_songs
#from .queueprocessor import QueueProcesser
from .forms import SchedulerForm

logger = logging.getLogger('alarmclock')

def alarms(request):
    logging.info("alarms request : %s",request)
    alarm_list = Alarms.objects.all()

    return render(request=request,template_name='alarmclock/alarms.html', context={'alarm_list':alarm_list})

class AlarmList(ListView):
    logger.debug("alarms list")
    model = Alarms
    context_object_name = 'alarm_list'
    queryset = Alarms.objects.order_by('-updated')

class AlarmCreate(CreateView):
    logger.info("create alarm")
    model = Alarms
    fields = ('name','day','daily','hour','total_songs','artist','playlist','active')
    success_url = reverse_lazy('alarmclock:alarms')

class AlarmDetails(DetailView):
    logger.debug("alarm details")
    model = Alarms
    context_object_name = 'alarm'

class AlarmUpdate(UpdateView):
    logger.info("update alarm")

    model = Alarms
    context_object_name = 'alarm'
    fields = ('name', 'day','daily','hour', 'total_songs', 'artist', 'playlist', 'active')

class AlarmDelete(DeleteView):
    logger.info("delete alarm")
    model = Alarms
    success_url = reverse_lazy('alarmclock:alarms')


def scheduler(request):

    logger.debug("scheduler request : %s", request)

    if request.method == 'POST':
        form = SchedulerForm(request.POST)
        return render(request=request, template_name='alarmclock/scheduler.html',context={'form':form,'status':'error'})

    else:
        logger.debug("get request from form")

        check_queue.delay()
       # play_queued_songs.delay()
        '''
        processer = QueueProcesser()
        processer.set_queued_songs()
        processer.play_queued_songs()
        #  logger.debug("available alarms: %s", schedule.get_scheduled_alarms())
        '''
        return render(request=request, template_name='alarmclock/scheduler.html',
                      context={'result': 'ok'})

