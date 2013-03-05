from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('snapshop.shop.urls')),
    url(r'^home/', 'snapshop.views.home', name='home'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^api/register', 'snapshop.views.api_register', name='api_register'),
    url(r'^api', 'snapshop.views.api', name='api'),
    # Examples:
    # url(r'^$', 'snapshop.views.home', name='home'),
    # url(r'^snapshop/', include('snapshop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
