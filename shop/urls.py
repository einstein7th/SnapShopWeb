from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('snapshop.shop.views',
    # url(r'^$', 'index', name="index"),
    # url(r'^main/$', 'main', name="main_main"),
    # url(r'^search/$', 'search', name="search"),
    # url(r'^thanks/$', 'thanks', name="thanks"),

    url(r'^$', 'search', name="search"),
    url(r'^results/$', 'results', name="results"),
    url(r'^sign-up/$', 'sign_up', name="sign_up"),
    url(r'^thanks/$', 'thanks', name="thanks"),
)

