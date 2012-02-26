import datetime
import hmac
import time
import uuid

from django.template.defaultfilters import slugify
import mongoengine
from mongoengine.django.auth import User

try:
    from hashlib import sha1
    sha1
except ImportError:
    import sha
    sha1 = sha.sha


class Variety(mongoengine.Document):
    """
    The different varieties of wine grapes
    """
    VARIETY_CHOICES = (
        ('red', 'Red'),
        ('white', 'White'),
    )
    name = mongoengine.StringField(max_length=255, unique=True, help_text="Varietal name")
    slug = mongoengine.StringField(unique=True)
    color = mongoengine.StringField(max_length=25, choices=VARIETY_CHOICES)
    description = mongoengine.StringField(default='None')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Variety, self).save(*args, **kwargs)


class Vineyard(mongoengine.Document):
    """
    Vineyard is a place that produces wine.

    Ensure you do the following in mongo to allow geospatial queries:
    > use krater_development
    > db.krater_vineyard.ensureIndex( { location : "2d" } )
    """

    # Embedded Models
    location = mongoengine.GeoPointField(help_text="Latitude and Longitude")

    # TTB Information
    permit_number = mongoengine.StringField(max_length=25, help_text="TTB Permit Number")
    owner_name = mongoengine.StringField(max_length=255, help_text="Vineyard Owner Name")
    operating_name = mongoengine.StringField(max_length=255, help_text="Vineyard Operating Name")
    street = mongoengine.StringField(max_length=255, help_text="Street Name")
    city = mongoengine.StringField(max_length=255, help_text="City Name")
    state = mongoengine.StringField(max_length=255, help_text="State Name")
    zipcode = mongoengine.StringField(max_length=10, help_text="Zip Code")
    county = mongoengine.StringField(max_length=255, help_text="County Name")

    # Extra Information
    slug = mongoengine.StringField(unique=True)
    url = mongoengine.URLField(verify_exists=False, help_text="Vineyard website")

    def __unicode__(self):
        return self.owner_name

    def save(self, *args, **kwargs):
        self.slug = slugify('%s %s %s' % (self.owner_name, self.operating_name, self.permit_number))
        if isinstance(self.location, (basestring, unicode)):
            self.location = [float(point) for point in self.location.strip('[]').split(',')]
        super(Vineyard, self).save(*args, **kwargs)


class Wine(mongoengine.Document):

    # Embedded Models
    variety = mongoengine.ReferenceField(Variety)
    vineyard = mongoengine.ReferenceField(Vineyard)

    name = mongoengine.StringField(max_length=200, help_text="Name of the wine")
    year = mongoengine.IntField(help_text="Year on label")
    appelation = mongoengine.StringField(max_length=200, help_text="Region of wine")

    composition = mongoengine.StringField(help_text="Composition of blended wines")
    aroma = mongoengine.StringField(help_text="Primary and secondary aromas")
    bouquet = mongoengine.StringField(help_text="Tertiary aromas")

    alcohol = mongoengine.FloatField(help_text="Alcohol by Volume")
    sulfites = mongoengine.BooleanField(default=False, help_text="Contains Sulfites")
    ta = mongoengine.FloatField("TA", help_text="titratable acidity")
    ph = mongoengine.FloatField("pH", help_text="pH")
    aging = mongoengine.StringField(max_length=200, help_text="Notes on aging")
    skin_contact = mongoengine.StringField(max_length=200, help_text="Duration of skin contact")

    def __unicode__(self):
        return "%s %s %s, %s" % (self.name, self.variety, self.year, self.vineyard)


class ApiAccess(mongoengine.Document):
    """A simple model for use with the ``CacheDBThrottle`` behaviors."""
    identifier = mongoengine.StringField()
    url = mongoengine.URLField()
    request_method = mongoengine.StringField()
    accessed = mongoengine.IntField()

    def __unicode__(self):
        return u"%s @ %s" % (self.identifer, self.accessed)

    def save(self, *args, **kwargs):
        self.accessed = int(time.time())
        return super(ApiAccess, self).save(*args, **kwargs)


class ApiKey(mongoengine.Document):

    user = mongoengine.ReferenceField(User)
    key = mongoengine.StringField()
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return u"%s for %s" % (self.key, self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        # Get a random UUID.
        new_uuid = uuid.uuid4()
        # Hmac that beast.
        return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()

    @classmethod
    def create_api_key(cls, sender, **kwargs):
        """
        A signal for hooking up automatic ``ApiKey`` creation.
        """
        if kwargs.get('created') is True:
            ApiKey.objects.get_or_create(user=kwargs.get('document'))

# Ensure API key is created for new users
mongoengine.signals.post_save.connect(ApiKey.create_api_key, sender=User)
