#! env/bin/python

import csv
import os
import sys

# Need to set up environment
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(os.path.join(cwd, 'project'))
sys.path.append(os.path.join(cwd, 'project', 'apps'))
os.environ['DJANGO_SETTINGS_MODULE'] = "project.settings"

from django.conf import settings

from apps.krater.models import Variety

# Set debug for printing
DEBUG = False

# Files to load
VARIETIES_RED = os.path.join(settings.PROJECT_ROOT, '..', 'data', 'varieties_red.csv')
VARIETIES_WHITE = os.path.join(settings.PROJECT_ROOT, '..', 'data', 'varieties_white.csv')


def main():
    for file_name in (VARIETIES_RED, VARIETIES_WHITE):
        csv_reader = csv.DictReader(open(file_name, 'rb'), delimiter=',', quotechar='"')
        for variety in csv_reader:
            if DEBUG:
                print variety
            v, created = Variety.objects.get_or_create(name=variety['NAME'].decode('utf-8'))
            v.color = variety['COLOR']
            v.description = variety['DESCRIPTION']
            v.save()
            if created:
                print 'Created: ', v
            else:
                print 'FOUND: ', v


if __name__ == "__main__":
    main()
