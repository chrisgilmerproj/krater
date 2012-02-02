from django.conf.urls.defaults import url, patterns
from piston.resource import Resource

from apps.api.handlers import WineHandler, VineyardHandler, VarietyHandler

wine_handler = Resource(WineHandler)
vineyard_handler = Resource(VineyardHandler)
variety_handler = Resource(VarietyHandler)

urlpatterns = patterns('',
    url(r'^wines/(?P<wine_id>[\w]+)/?$', wine_handler),
    url(r'^wines/?$', wine_handler),

    url(r'^vineyards/(?P<vineyard_id>[\w]+)/?$', vineyard_handler),
    url(r'^vineyards/?$', vineyard_handler),

    url(r'^varieties/(?P<variety_id>[\w]+)/?$', variety_handler),
    url(r'^varieties/?$', variety_handler),
)
