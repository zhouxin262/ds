from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ds.views.home', name='home'),
	(r'^accounts/', include('registration.backends.default.urls')),
    # Examples:
    # url(r'^$', 'ds.views.home', name='home'),
    # url(r'^ds/', include('ds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
