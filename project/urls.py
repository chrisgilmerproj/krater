from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from tastypie.api import Api

from apps.krater.api import VarietyResource, VineyardResource, WineResource

v1_api = Api(api_name='v1')
v1_api.register(VarietyResource())
v1_api.register(VineyardResource())
v1_api.register(WineResource())

urlpatterns = patterns('',
    (r'^admin/', include('mongonaut.urls')),

    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name="home"),
    url(r'^api/', include(v1_api.urls)),
)

# Static URLs
urlpatterns += staticfiles_urlpatterns()

# Upload URLS
if settings.DEBUG:
    urlpatterns.insert(-2, url(r'^%s(?P<path>.*)' % settings.MEDIA_URL[1:],
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
