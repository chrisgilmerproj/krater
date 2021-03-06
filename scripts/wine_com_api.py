#! /usr/local/bin/python

import simplejson as json
import os

import requests

DEBUG = True


class WineProduct(object):

    def __init__(self, data):
        self.raw_data = data

        self.id = data['Id']
        self.name = data['Name']
        self.description = data['Description']
        self.geo_location = data['GeoLocation']
        self.url = data['Url']
        self.price_min = float(data['PriceMin'])
        self.price_max = float(data['PriceMax'])
        self.price_retail = float(data['PriceRetail'])
        self.type = data['Type']
        if 'Year' in data:
            self.year = int(data['Year'])
        else:
            self.year = 0
        self.appellation = data['Appellation']
        self.varietal = data['Varietal']
        self.vineyard = data['Vineyard']
        if 'Product' in data:
            self.product = data['Product']
        else:
            self.product = ''
        self.labels = data['Labels']
        self.ratings = data['Ratings']
        self.retail = data['Retail']
        self.vintages = data['Vintages']
        self.community = data['Community']

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.__unicode__()


class WineProducts(object):

    data_key = 'Products'

    def __init__(self, data):
        self.raw_data = data[self.data_key]
        self.total = self.raw_data['Total']
        self.offset = self.raw_data['Offset']
        self.url = self.raw_data['Url']
        self.list = self.raw_data['List']
        self.set_products()

    def set_products(self):
        self.products = [WineProduct(item) for item in self.list]


class Refinement(object):

    def __init__(self, data):
        self.raw_data = data
        self.id = data['Id']
        self.name = data['Name']
        self.url = data['Url']

    def __unicode__(self):
        return "(%s, %s)" % (self.name, self.id)

    def __repr__(self):
        return self.__unicode__()


class WineCategory(object):

    def __init__(self, data):
        self.raw_data = data
        self.id = data['Id']
        self.name = data['Name']
        self.refinements = [Refinement(item) for item in data['Refinements']]

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.__unicode__()


class WineCategories(object):

    data_key = 'Categories'

    def __init__(self, data):
        self.raw_data = data[self.data_key]
        self.set_categories()

    def set_categories(self):
        self.categories = [WineCategory(item) for item in self.raw_data]


class WineApiConnection(object):
    API_ENDPOINT = "http://services.wine.com/api/beta2/service.svc"
    FORMAT_TYPES = ['xml', 'json']
    RESOURCE_LIST = ['catalog', 'categorymap', 'reference']

    def __init__(self, api_key='', format='json'):

        if not api_key:
            self.api_key = self.get_api_key()
        else:
            self.api_key = api_key

        self.set_format(format)

    def set_format(self, format):
        if format not in self.FORMAT_TYPES:
            raise Exception('Invalid format. Must use one of %s' % self.FORMAT_TYPES)
        self.format = format

    def get_api_key(self):
        try:
            return os.environ['WINE_API_KEY']
        except KeyError:
            return ""

    def get_url_endpoint(self):
        if self.resource not in self.RESOURCE_LIST:
            raise Exception('Invalid resource. Must use one of %s' % self.RESOURCE_LIST)
        return os.path.join(self.API_ENDPOINT, self.format, self.resource)

    def update_payload(self, payload):
        payload.update({
            'apikey': self.api_key,
            })

    def check_status(self, data):
        status = data['Status']
        messages = status['Messages']
        code = status['ReturnCode']
        if DEBUG and code != 0:
            print 'Status %d: %s' % (code, '\n'.join(messages))
        if code == 0:
            pass
        elif code == 100:
            raise Exception('A critical error was encountered. This is due to a bug in the service. Please notify wine.com ASAP to correct this issue.')
        elif code == 200:
            raise Exception('Unable to Authorize. We cannot authorize this account.')
        elif code == 300:
            raise Exception('No Access. Account does not have access to this service.')

    def get(self, **kwargs):
        url = self.get_url_endpoint()
        self.update_payload(kwargs)
        r = requests.get(url, params=kwargs)
        data = json.loads(r.content)
        if DEBUG:
            print r.url
        self.check_status(data)
        return self.data_cls(data)


class CategoryMapApi(WineApiConnection):

    resource = 'categorymap'
    data_key = 'Categories'
    data_cls = WineCategories

    def __init__(self, api_key='', format='json',
                       filter='', search=''):
        self.filter = ''
        super(CategoryMapApi, self).__init__(api_key, format)

    def update_payload(self, payload):
        if self.filter:
            payload['filter'] = self.filter
        super(CategoryMapApi, self).update_payload(payload)

    def search(self, query, **kwargs):
        payload = {
            'search': '+'.join(query.split()),
        }
        kwargs.update(payload)
        return self.get(**kwargs)


class ProductApi(WineApiConnection):

    resource = 'catalog'
    data_key = 'Products'
    data_cls = WineProducts
    SORT_TYPES = ['popularity', 'rating', 'vintage', 'winery', 'name', 'price', 'saving', 'justIn']

    def __init__(self, api_key='', format='json', offset=0, size=25,
                       sort='rating', direction='ascending',
                       state='CA', instock=True,
                       filter='', search=''):
        self.offset = offset
        self.size = size
        self.state = state
        self.instock = instock
        self.filter = ''
        self.set_sort(sort, direction)
        super(ProductApi, self).__init__(api_key, format)

    def set_sort(self, sort='rating', direction='ascending'):
        if sort not in self.SORT_TYPES:
            raise Exception('Invalid sort. Must use one of %s' % self.SORT_TYPES)
        if direction not in ['ascending', 'descending']:
            raise Exception('Sort direction must be ascending or descending')
        self.sort = '%s|%s' % (sort, direction)

    def set_filters(self, categories=None, rating=None, price=None, product=None):
        filters = []
        if categories:
            filters.append('categories(%s)' % categories)
        if rating:
            filters.append('rating(%s)' % rating)
        if price:
            filters.append('price(%s)' % price)
        if product:
            filters.append('product(%s)' % product)
        self.filter = '+'.join(filters)

    def update_payload(self, payload):
        payload.update({
            'offset': str(self.offset),
            'size': str(self.size),
            'sort': self.sort,
            'state': self.state,
            'instock': str(self.instock).lower(),
            })
        if self.filter:
            payload['filter'] = self.filter
        super(ProductApi, self).update_payload(payload)

    def search(self, query, **kwargs):
        payload = {
            'search': '+'.join(query.split()),
        }
        kwargs.update(payload)
        return self.get(**kwargs)


def main():

    api = ProductApi()
    api.set_filters(rating='85|100')
    wine_products = api.search("7 Deadly Zins")
    product = wine_products.products[0]
    print product

    api = CategoryMapApi()
    wine_categories = api.get()
    category = wine_categories.categories[0]
    refinements = category.refinements
    print refinements

if __name__ == "__main__":
    main()
