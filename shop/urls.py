from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('snapshop.shop.views',
    url(r'^$', 'index', name="index"),
    url(r'^main/$', 'main', name="main_main"),
    url(r'^search/$', 'search', name="search"),
    url(r'^thanks/$', 'thanks', name="thanks"),
)

