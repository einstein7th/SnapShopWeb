from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('snapshop.shop.views',
    url(r'^$', 'index', name="index"),
    url(r'^search/$', 'search', name="search"),
)

