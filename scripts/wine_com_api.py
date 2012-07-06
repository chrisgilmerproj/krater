#! /usr/local/bin/python

import simplejson as json
import os
import pprint

import requests

DEBUG = True


class WineApi(object):
    API_ENDPOINT = "http://services.wine.com/api/beta2/service.svc"
    RESOURCE_LIST = ["catalog", "reference", "categorymap"]
    RESOURCE_TO_DATA_MAP = {
        'catalog': 'Products',
        'categorymap': 'Categories',
        'reference': 'Books',
    }

    def __init__(self, format='json', offset=0, size=25, sort='ascending', api_key=''):
        self.format = format
        self.offset = offset
        self.size = size
        self.sort = 'ascending'
        if not api_key:
            self.api_key = self.get_api_key()
        else:
            self.api_key = api_key

    def get_api_key(self):
        try:
            return os.environ['WINE_API_KEY']
        except KeyError:
            return ""

    def get_url_endpoint(self, resource):
        if resource not in self.RESOURCE_LIST:
            raise Exception('Invalid resource. Must use one of %s' % self.RESOURCE_LIST)
        return os.path.join(self.API_ENDPOINT, self.format, resource)

    def get_payload(self, payload):
        payload.update({
            'offset': str(self.offset),
            'size': str(self.size),
            'sort': self.sort,
            'apikey': self.api_key,
            })
        return payload

    def verify_message(self, data):
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

    def get_data(self, resource, data):
        self.verify_message(data)
        key = self.RESOURCE_TO_DATA_MAP[resource]
        return data[key]

    def get(self, resource, **kwargs):
        url = self.get_url_endpoint(resource)
        r = requests.get(url, params=self.get_payload(kwargs))
        data = json.loads(r.content)
        if DEBUG:
            print r.url
        return self.get_data(resource, data)

    def search(self, query):
        payload = {
            'search': '+'.join(query.split()),
        }
        return self.get('catalog', **payload)


def main():

    api = WineApi()
    data = api.search("7 Deadly Zins")
    data = data['List'][0]
    pprint.pprint(data)


if __name__ == "__main__":
    main()
