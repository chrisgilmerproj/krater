from django.contrib import admin

from apps.krater.models import Point, Variety, Vineyard, Wine

admin.site.register(Point)
admin.site.register(Variety)
admin.site.register(Vineyard)
admin.site.register(Wine)
