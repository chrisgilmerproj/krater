from django.db import models
from django.template.defaultfilters import slugify

from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager
from django.contrib.localflavor.us.models import USStateField


class Point(models.Model):
    """
    A geographical location given by latitude and longitude
    """
    latitude = models.FloatField()
    longitude = models.FloatField()

    objects = MongoDBManager()

    def __unicode__(self):
        return "lat/lon - %s/%s" % (self.latitude, self.longitude)


class Variety(models.Model):
    """
    The different varieties of wine grapes
    """
    VARIETY_CHOICES = (
        ('red', 'Red'),
        ('white', 'White'),
    )
    name = models.CharField(max_length=255, unique=True, help_text="Varietal name")
    slug = models.SlugField(editable=False, unique=True)
    color = models.CharField(max_length=25, choices=VARIETY_CHOICES)
    description = models.TextField()

    objects = MongoDBManager()

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Variety, self).save(*args, **kwargs)


class Vineyard(models.Model):
    """
    Vineyard is a place that produces wine.

    Ensure you do the following in mongo to allow geospatial queries:
    > use krater_development
    > db.krater_vineyard.ensureIndex( { location : "2d" } )
    """

    # Embedded Models
    location = EmbeddedModelField(Point, blank=True, null=True)

    # TTB Information
    permit_number = models.CharField(max_length=25, help_text="TTB Permit Number")
    owner_name = models.CharField(max_length=255, help_text="Vineyard Owner Name")
    operating_name = models.CharField(max_length=255, help_text="Vineyard Operating Name")
    street = models.CharField(max_length=255, help_text="Street Name")
    city = models.CharField(max_length=255, help_text="City Name")
    state = USStateField()
    zipcode = models.CharField(max_length=10, help_text="Zip Code")
    county = models.CharField(max_length=255, help_text="County Name")

    # Extra Information
    slug = models.SlugField(editable=False, unique=True)
    url = models.URLField(verify_exists=True, help_text="Vineyard website")

    objects = MongoDBManager()

    class Meta:
        ordering = ['owner_name', ]

    def __unicode__(self):
        return self.owner_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.owner_name)
        super(Vineyard, self).save(*args, **kwargs)


class Wine(models.Model):

    # Embedded Models
    variety = EmbeddedModelField('Variety')
    vineyard = EmbeddedModelField('Vineyard')

    name = models.CharField(max_length=200, help_text="Name of the wine")
    year = models.PositiveIntegerField(help_text="Year on label")
    appelation = models.CharField(max_length=200, blank=True, help_text="Region of wine")

    composition = models.TextField(blank=True, help_text="Composition of blended wines")
    aroma = models.TextField(blank=True, help_text="Primary and secondary aromas")
    bouquet = models.TextField(blank=True, help_text="Tertiary aromas")

    alcohol = models.FloatField(blank=True, null=True, help_text="Alcohol by Volume")
    sulfites = models.BooleanField(default=False, help_text="Contains Sulfites")
    ta = models.FloatField("TA", blank=True, null=True, help_text="titratable acidity")
    ph = models.FloatField("pH", blank=True, null=True, help_text="pH")
    aging = models.CharField(max_length=200, blank=True, help_text="Notes on aging")
    skin_contact = models.CharField(max_length=200, blank=True, help_text="Duration of skin contact")

    objects = MongoDBManager()

    class Meta:
        ordering = ['variety', 'name', ]

    def __unicode__(self):
        return "%s %s %s, %s" % (self.name, self.variety, self.year, self.vineyard)
