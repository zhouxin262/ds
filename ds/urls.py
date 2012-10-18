from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ds.views.home', name='home'),
    url(r'^user/add/$', 'ds.views.adduser', name='adduser'),
    url(r'^user/list/$', 'ds.views.listuser', name='listuser'),
    url(r'^user/(?P<id>\d+)/del/$', 'ds.views.deluser', name='deluser'),
    url(r'^user/(?P<id>\d+)/edit/$', 'ds.views.edituser', name='edituser'),

    (r'^gongzi/', include('gongzi.urls')),
    (r'^webstatus/', include('webstatus.urls')),
	(r'^accounts/', include('registration.backends.simple.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
