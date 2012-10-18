from django.conf.urls import patterns, url, include
from django.views.generic import list_detail
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$|create/$',  'webstatus.views.create', name='webstatus_create'),
    url(r'^list/$',  'webstatus.views.list', name='webstatus_list'),
    url(r'^(?P<id>\d+)/view/$',  'webstatus.views.view', name='webstatus_view'),
    url(r'^(?P<id>\d+)/update/$',  'webstatus.views.update', name='webstatus_update'),
    url(r'^(?P<id>\d+)/delete/$',  'webstatus.views.delete', name='webstatus_delete'),
)