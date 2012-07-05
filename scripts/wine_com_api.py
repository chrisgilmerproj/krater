#! /usr/local/bin/python

import simplejson as json
import os
import pprint

import requests


FORMAT = 'json'
API_ENDPOINT = "http://services.wine.com/api/beta2/service.svc"
RESOURCE_LIST = ["catalog", "reference", "categorymap"]


def main():
    try:
        api_key = os.environ['WINE_API_KEY']
    except KeyError:
        api_key = ""

    payload = {
        'offset': '0',
        'size': '25',
        'sort': 'ascending',
        'instock': 'false',
        'filter': 'categories(490)',
        'apikey': api_key,
    }

    url = os.path.join(API_ENDPOINT, FORMAT, "categorymap")
    r = requests.get(url, params=payload)
    data = json.loads(r.content)
    categories = [(d['Name'], d['Id']) for d in data['Categories']]
    print categories
    print r.url


if __name__ == "__main__":
    main()
