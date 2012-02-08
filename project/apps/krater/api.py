from tastypie.resources import ModelResource
from apps.krater.models import Variety, Vineyard, Wine


class VarietyResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Variety.objects.all()
        #Variety._meta['fields'] = Variety._fields
        queryset.model = Variety
        resource_name = 'variety'
        fields = ('id',
                  'name',
                  'slug',
                  'color',
                  'description',
                 )


class VineyardResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Vineyard.objects.all()
        resource_name = 'vineyard'
        fields = ('id',
                  'permit_number',
                  'owner_name',
                  'operating_name',
                  'street',
                  'city',
                  'state',
                  'zipcode',
                  'county',
                  'slug',
                  'url',
                  'location',
                 )

    def get_object_list(self, request):
        # Limit query results
        limit = request.GET.get('limit', 20)
        if limit > 100:
            limit = 100
        elif limit < 0:
            limit = 1

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
        return super(VineyardResource, self).get_object_list(request)


class WineResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Wine.objects.all()
        resource_name = 'wine'
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
                  'vineyard',
                  'variety',
                 )
