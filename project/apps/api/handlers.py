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
              'permit_number',
              'owner_name',
              'operating_name',
              'street',
              'state',
              'zipcode',
              'county',
              'slug',
              'url',
              ('location', ('latitude', 'longitude')),
             )

    def read(self, request, vineyard_id=None):

        # Limit query results
        limit = request.GET.get('limit', 20)
        if limit > 100:
            limit = 100
        elif limit < 0:
            limit = 1

        if vineyard_id:
            return Vineyard.objects.get(id=vineyard_id)

        if request.GET.get('geo', False):
            lat = float(request.GET.get('lat'))
            lon = float(request.GET.get('lon'))
            radius = float(request.GET.get('radius', 10))
            units = request.GET.get('units', 'km')

            # Must convert radius and units into degrees
            # Given 10km we 10km * degrees/111.0km
            # Given 10mi we 10mi * degrees/69.0mi
            if units == 'km':
                radius = radius / 111.0
            elif units == 'm':
                radius = radius / (111.0 * 1000.0)  # 1000m per km
            elif units == 'mi':
                radius = radius / 69.0
            elif units == 'ft':
                radius = radius / (69.0 * 5280.0)  # 5280ft per mi
            else:
                raise Exception('Units are wrong')
            center = {'latitude': lat, 'longitude': lon}

            #return Vineyard.objects.raw_query({'location' : {'$near' : here}})
            return Vineyard.objects.raw_query({"location": {"$within": {"$center": [center, radius]}}})[:limit]

        return Vineyard.objects.all()[:limit]


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
