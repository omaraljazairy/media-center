from django.conf.urls import url
from . import views

app_name = 'alarmclock'

urlpatterns = [
    url(r'alarms/$',views.AlarmList.as_view(), name='alarms'),
    url(r'alarm/details/(?P<pk>[0-9]+)/$', views.AlarmDetails.as_view(), name='alarm_details'),
    url(r'alarm/add/$', views.AlarmCreate.as_view(), name='alarm_add'),
    url(r'alarm/edit/(?P<pk>[0-9]+)/$', views.AlarmUpdate.as_view(), name='alarm_edit'),
    url(r'alarm/delete/(?P<pk>[0-9]+)/$', views.AlarmDelete.as_view(), name='alarm_delete'),

]