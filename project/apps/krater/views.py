from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
import requests

GOOGLE_SHOPPING_API = 'https://www.googleapis.com/shopping/search/v1/public/products'


def product_search(request):
    if 'name' not in request.GET or 'type' not in request.GET:
        return HttpResponseBadRequest('Missing parameters, need both name and type')
    name = request.GET['name']
    type = request.GET['type']
    query = '+'.join(name.split() + type.split())
    params = {
        'key': settings.GOOGLE_SIMPLE_API_KEY,
        'country': 'US',
        'q': query,
        'alt': 'json',
    }
    r = requests.get(GOOGLE_SHOPPING_API, params=params)
    if r.status_code != 200:
        return HttpResponseBadRequest('Something went wrong with Google shopping api')
    return HttpResponse(r.text, mimetype="application/json")
