#! /usr/local/bin/python

import simplejson as json
import os
import pprint

import requests


try:
    api_key = os.environ['WINE_API_KEY']
except KeyError:
    api_key = ""

FORMAT = 'json'
API_ENDPOINT = "http://services.wine.com/api/beta2/service.svc"
RESOURCE_LIST = ["catalog", "reference", "categorymap"]
DEFAULTS = {
    'offset': '0',
    'size': '25',
    'sort': 'ascending',
    'apikey': api_key,
}


def get_url_endpoint(resource):
    if resource not in RESOURCE_LIST:
        raise Exception('Must use one of %s' % RESOURCE_LIST)
    return os.path.join(API_ENDPOINT, FORMAT, resource)


def get_payload(payload):
    payload.update(DEFAULTS)
    return payload


def main():

    payload = {
        'filter': 'categories(490)',
    }

    url = get_url_endpoint("categorymap")
    r = requests.get(url, params=get_payload(payload))
    data = json.loads(r.content)
    categories = [(d['Name'], d['Id']) for d in data['Categories']]
    pprint.pprint(categories)
    print r.url

    payload = {
        'search': '+'.join('7 Deadly Zins'.split()),
    }

    url = get_url_endpoint("catalog")
    r = requests.get(url, params=get_payload(payload))
    data = json.loads(r.content)['Products']['List'][0]
    pprint.pprint(data)
    print r.url


if __name__ == "__main__":
    main()
