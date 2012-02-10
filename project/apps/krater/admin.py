from django.contrib import admin

from apps.krater.models import Variety, Vineyard, Wine

admin.site.register(Variety)
admin.site.register(Vineyard)
admin.site.register(Wine)
