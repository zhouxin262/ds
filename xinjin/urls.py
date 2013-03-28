from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^all/$',  'xinjin.views.all', name='xinjindan_all'),
    url(r'^$|list/$',  'xinjin.views.list', name='xinjindan_list'),
    url(r'^create/$',  'xinjin.views.create', name='xinjindan_create'),
    url(r'^(?P<id>\d+)/update/$',  'xinjin.views.update', name='xinjindan_update'),
    url(r'^(?P<id>\d+)/delete/$',  'xinjin.views.delete', name='xinjindan_delete'),

    url(r'^(?P<id>\d+)/$',  'xinjin.views.xinjin_list', name='xinjin_list'),
    url(r'^(?P<id>\d+)/create/$',  'xinjin.views.xinjin_create', name='xinjin_create'),
    url(r'^(?P<id>\d+)/(?P<xid>\d+)/update/$',  'xinjin.views.xinjin_update', name='xinjin_update'),
    url(r'^(?P<id>\d+)/(?P<xid>\d+)/delete/$',  'xinjin.views.xinjin_delete', name='xinjin_delete'),
    url(r'^(?P<id>\d+)/(?P<xid>\d+)/valid/$',  'xinjin.views.xinjin_valid', name='xinjin_valid'),
)
