from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'gongzi.views.home', name='gongzi_home'),
                       url(r'^query/$', 'gongzi.views.query', name='gongzi_query'),
                       url(r'^admin/upload/$', 'gongzi.views.upload', name='gongzi_upload'),
                       url(r'^admin/create/$', 'gongzi.views.create', name='gongzi_create'),
                       url(r'^admin/list/$', 'gongzi.views.list', name='gongzi_list'),
                       url(r'^admin/bulk_delete/$', 'gongzi.views.bulk_delete', name='gongzi_bulk_delete'),
                       url(r'^admin/(?P<id>\d+)/update/$', 'gongzi.views.update', name='gongzi_update'),
                       url(r'^admin/(?P<id>\d+)/delete/$', 'gongzi.views.delete', name='gongzi_delete'),
                       )
