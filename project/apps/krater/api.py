from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
import mongoengine

from apps.krater.fields import ListField, DictField
from apps.krater.models import Variety, Vineyard, Wine


class MongoResource(ModelResource):

    def get_object_list(self, request):
        return self._meta.queryset

    @classmethod
    def get_fields(cls, fields=None, excludes=None):
        """
        Given any explicit fields to include and fields to exclude, add
        additional fields based on the associated model.
        """
        final_fields = {}
        fields = fields or []
        excludes = excludes or []

        if not cls._meta.object_class:
            return final_fields

        for n, f in cls._meta.object_class._fields.iteritems():

            # If the field name is already present, skip
            if f.name in cls.base_fields:
                continue

            # If field is not present in explicit field listing, skip
            if fields and f.name not in fields:
                continue

            # If field is in exclude list, skip
            if excludes and f.name in excludes:
                continue

            api_field_class = cls.api_field_from_mongo_field(f)

            kwargs = {
                'attribute': f.name,
                'help_text': f.help_text,
            }

            kwargs['unique'] = f.unique

            if f.default:
                kwargs['default'] = f.default

            final_fields[f.name] = api_field_class(**kwargs)
            final_fields[f.name].instance_name = f.name

        return final_fields

    @classmethod
    def api_field_from_mongo_field(cls, f, default=fields.CharField):
        """
        Returns the field type that would likely be associated with each
        Mongo type.
        """
        result = default

        if isinstance(f, (mongoengine.DateTimeField, mongoengine.ComplexDateTimeField)):
            result = fields.DateTimeField
        elif isinstance(f, mongoengine.BooleanField):
            result = fields.BooleanField
        elif isinstance(f, mongoengine.FloatField):
            result = fields.FloatField
        elif isinstance(f, mongoengine.DecimalField):
            result = fields.DecimalField
        elif isinstance(f, mongoengine.IntField):
            result = fields.IntegerField
        elif isinstance(f, mongoengine.FileField):
            result = fields.FileField
        elif isinstance(f, mongoengine.ListField):
            result = ListField
        elif isinstance(f, mongoengine.DictField):
            result = DictField
        #elif isinstance(f, mongoengine.EmbeddedDocumentField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.ObjectIdField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.ReferenceField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.MapField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.URLField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.GenericReferenceField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.BinaryField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.SortedListField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.EmailField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.GeoPointField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.SequenceField):
        #    result = fields.??
        #elif isinstance(f, mongoengine.GenericEmbeddedDocumentField):
        #    result = fields.??
        return result


class VarietyResource(MongoResource):
    class Meta:
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        queryset = Variety.objects
        queryset.model = Variety
        resource_name = 'variety'
        serializer = Serializer(['json', 'xml', 'yaml'])
        fields = ('id',
                  'name',
                  'slug',
                  'color',
                  'description',
                 )


class VineyardResource(MongoResource):
    class Meta:
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        queryset = Vineyard.objects
        queryset.model = Vineyard
        resource_name = 'vineyard'
        serializer = Serializer(['json', 'xml', 'yaml'])
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
                raise Exception('Units must be km/m/mi/ft')
            #center = {'latitude': lat, 'longitude': lon}
            #return Vineyard.objects(__raw__={"location": {"$within": {"$center": [center, radius]}}})[:limit]
            return Vineyard.objects(location__within_distance=[(lat, lon), radius])[:limit]
        return super(VineyardResource, self).get_object_list(request)[:limit]


class WineResource(MongoResource):
    class Meta:
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        queryset = Wine.objects
        queryset.model = Wine
        resource_name = 'wine'
        serializer = Serializer(['json', 'xml', 'yaml'])
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
