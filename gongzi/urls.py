from django.conf.urls import patterns, url, include
from django.views.generic import list_detail
from gongzi.models import Gongzi
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gongzi.views.home', name='gongzi_home'),
    url(r'^upload/$', 'gongzi.views.upload', name='gongzi_upload'),
    url(r'^admin/list/$',  'gongzi.views.list', name='gongzi_list'),
    url(r'^admin/(?P<id>\d+)/view/$',  'gongzi.views.view', name='gongzi_view'),
    url(r'^admin/(?P<id>\d+)/update/$',  'gongzi.views.update', name='gongzi_update'),
    url(r'^admin/(?P<id>\d+)/delete/$',  'gongzi.views.delete', name='gongzi_delete'),

)