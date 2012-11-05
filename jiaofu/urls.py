from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$|list/$',  'jiaofu.views.list', name='zixun_list'),
    url(r'^create/$',  'jiaofu.views.create', name='zixun_create'),
    url(r'^(?P<id>\d+)/$',  'jiaofu.views.view', name='zixun_view'),
    url(r'^(?P<id>\d+)/update/$',  'jiaofu.views.update', name='zixun_update'),
    url(r'^(?P<id>\d+)/delete/$',  'jiaofu.views.delete', name='zixun_delete'),
)
