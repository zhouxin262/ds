from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gongzi.views.home', name='gongzi_home'),
    url(r'^upload/$', 'gongzi.views.upload', name='gongzi_upload'),
    )