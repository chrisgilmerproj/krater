from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('krater.views',
    url(r'^product_search/$', 'product_search', name='product_search'),
)
