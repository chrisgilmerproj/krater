from mongonaut.sites import MongoAdmin

from apps.krater.models import Variety, Vineyard, Wine


class NewAdmin(MongoAdmin):

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request):
        return True

    def has_edit_permission(self, request):
        return True

    def has_view_permission(self, request):
        return True

Variety.mongoadmin = NewAdmin()
Vineyard.mongoadmin = NewAdmin()
Wine.mongoadmin = NewAdmin()
