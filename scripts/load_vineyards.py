#! env/bin/python

import csv
import os
import string
import sys

# Need to set up environment
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(os.path.join(cwd, 'project'))
sys.path.append(os.path.join(cwd, 'project', 'apps'))
os.environ['DJANGO_SETTINGS_MODULE'] = "project.settings"

from django.conf import settings

from apps.krater.models import Vineyard

# Set debug for printing
DEBUG = False

# Files to load
VINEYARDS_USA = os.path.join(settings.PROJECT_ROOT, '..', 'data', 'vineyards_usa.csv')
VINEYARDS_CA = os.path.join(settings.PROJECT_ROOT, '..', 'data', 'vineyards_california.csv')


def main():
    for file_name in (VINEYARDS_USA, VINEYARDS_CA):
        csv_reader = csv.DictReader(open(file_name, 'rb'), delimiter=',', quotechar='"')
        for vineyard in csv_reader:
            for key in ['OPERATING NAME', 'OWNER NAME', 'STREET', 'CITY', 'COUNTY']:
                name = vineyard[key]
                name = string.replace(name, '\xc2\xa0', '')  # Spaces are translated to this
                name = string.capwords(name)  # Change the input to capwords
                if 'Llc' in name:  # Fix capwords LLC
                    name = string.replace(name, 'Llc', 'LLC')
                vineyard[key] = name

            # Ensure that operating name is not empty
            if vineyard['OPERATING NAME'] == '':
                vineyard['OPERATING NAME'] = vineyard['OWNER NAME']

            if DEBUG:
                print vineyard
            v, created = Vineyard.objects.get_or_create(permit_number=vineyard['PERMIT NUMBER'])
            v.owner_name = vineyard['OWNER NAME']
            v.operating_name = vineyard['OPERATING NAME']
            v.street = vineyard['STREET']
            v.city = vineyard['CITY']
            v.state = vineyard['STATE']
            v.zipcode = vineyard['ZIP'] + '-' + vineyard['ZIP4']
            v.county = vineyard['COUNTY']
            v.save()
            if created:
                print 'Created: ', v
            else:
                print 'FOUND: ', v


if __name__ == "__main__":
    main()
