from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^done/$', 'done', name='done'),
    url(r'^error/$', 'error', name='error'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^form/$', 'form', name='form'),
)
