from django.template.defaultfilters import slugify

import mongoengine


class Point(mongoengine.EmbeddedDocument):
    """
    A geographical location given by latitude and longitude
    """
    latitude = mongoengine.FloatField()
    longitude = mongoengine.FloatField()

    def __unicode__(self):
        return "lat/lon - %s/%s" % (self.latitude, self.longitude)


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
    description = mongoengine.StringField()

    class Meta:
        ordering = ['name', ]

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
    location = mongoengine.EmbeddedDocumentField(Point)

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
    url = mongoengine.URLField(verify_exists=True, help_text="Vineyard website")

    class Meta:
        ordering = ['owner_name', ]

    def __unicode__(self):
        return self.owner_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.owner_name)
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

    class Meta:
        ordering = ['variety', 'name', ]

    def __unicode__(self):
        return "%s %s %s, %s" % (self.name, self.variety, self.year, self.vineyard)
