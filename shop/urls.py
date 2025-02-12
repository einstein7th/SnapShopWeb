from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('snapshop.shop.views',
    url(r'^$', 'search', name="search"),
    url(r'^results/$', 'results', name="results"),
    url(r'^sign-up/$', 'sign_up', name="sign_up"),
    url(r'^thanks/$', 'thanks', name="thanks"),
    url(r'^save_cart/$', 'save_cart', name="save_cart"),
    url(r'^view-item/(?P<item_id>.*)/$', 'view_item', name="view_item"),
    url(r'^account/$', 'account', name="account"),
    url(r'^browse/$', 'category_view', name="category_view"),
)

