from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import login
# from django.contrib.auth import logout # logout is unnecssary to import?

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('snapshop.shop.urls')),
    url(r'^home/', 'snapshop.views.home', name='home'),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    # temporary logout fix: Otherwise directs to Django admin logout instead of
    # auth.views.logout (that would use registration/logged_out.html template)

    # Examples:
    # url(r'^$', 'snapshop.views.home', name='home'),
    # url(r'^snapshop/', include('snapshop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
