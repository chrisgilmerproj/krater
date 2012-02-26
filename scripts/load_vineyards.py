#! env/bin/python

import csv
import os
import string

from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = "project.settings"

VINEYARDS_USA = os.path.join(settings.PROJECT_ROOT, '..', 'data', 'vineyards_usa.csv')
VINEYARDS_CA = os.path.join(settings.PROJECT_ROOT, '..', 'data', 'vineyards_california.csv')


def main():
    for file_name in (VINEYARDS_USA, VINEYARDS_CA):
        csv_reader = csv.DictReader(open(file_name, 'rb'), delimiter=',', quotechar='"')
        for vineyard in csv_reader:
            for key in ['OPERATING NAME', 'OWNER NAME', 'STREET', 'CITY', 'COUNTY']:
                name = string.capwords(vineyard[key])
                if 'Llc' in name:
                    name = string.replace(name, 'Llc', 'LLC')
                vineyard[key] = name
            if vineyard['OPERATING NAME'] == '\xc2\xa0':
                vineyard['OPERATING NAME'] = vineyard['OWNER NAME']
            print vineyard


if __name__ == "__main__":
    main()
