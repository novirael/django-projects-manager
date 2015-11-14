from django.conf.urls import patterns, url
from django.contrib import admin

from .views import (
    ProjectCreate,
    ProjectIndex,
    ProjectDetails,
    SyncWithTrello,
    TaskCreate,
    TaskDetails,
    TaskStartTimer,
    TaskStopTimer,
)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', ProjectIndex.as_view(), name='index'),

    url(r'^create-project/$', ProjectCreate.as_view(), name='create_project'),
    url(r'^create-task/$', TaskCreate.as_view(), name="create_task"),
    url(r'^details/(?P<id>\d+)/$', ProjectDetails.as_view(), name='details'),
    url(r'^details-task/(?P<id>\d+)/$', TaskDetails.as_view(), name='task_details'),
    url(r'^task/(?P<id>\d+)/start/$', TaskStartTimer.as_view(), name="start"),
    url(r'^task/(?P<id>\d+)/stop/$', TaskStopTimer.as_view(), name="stop"),

    url(r'^sync/(?P<id>\d+)/$', SyncWithTrello.as_view(), name="sync"),
)
