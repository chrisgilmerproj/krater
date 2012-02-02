from piston.handler import BaseHandler

from apps.krater.models import Wine, Vineyard, Variety


class WineHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Wine
    fields = ('id',
              'name',
              'year',
              'appelation',
              'composition',
              'aroma',
              'bouquet',
              'alcohol',
              'sulfites',
              'ta',
              'ph',
              'aging',
              'skin_contact',
              ('vineyard', ('id', 'name', 'slug', 'url', 'location')),
              ('variety', ('id', 'name',)),
             )

    def read(self, request, wine_id=None):
        if wine_id:
            return Wine.objects.get(id=wine_id)
        return Wine.objects.all()


class VineyardHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Vineyard
    fields = ('id',
              'name',
              'slug',
              'url',
              'location',
             )

    def read(self, request, vineyard_id=None):
        if vineyard_id:
            return Vineyard.objects.get(id=vineyard_id)
        return Vineyard.objects.all()


class VarietyHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Vineyard
    fields = ('id',
              'name',
             )

    def read(self, request, variety_id=None):
        if variety_id:
            return Variety.objects.get(id=variety_id)
        return Variety.objects.all()
