from django.db import models
from django.template.defaultfilters import slugify

from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager


class Point(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Variety(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Varietal name")

    objects = MongoDBManager()

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class Vineyard(models.Model):
    """
    Vineyard is a place that produces wine.

    Ensure you do the following in mongo to allow geospatial queries:
    > use krater_vineyard
    > db.krater_vineyard.ensureIndex( { location : "2d" } )
    """

    # Embedded Models
    location = EmbeddedModelField(Point, null=True)

    name = models.CharField(max_length=200, help_text="Vineyard name")
    slug = models.SlugField(editable=False, unique=True)
    url = models.URLField(verify_exists=True, help_text="Vineyard website")

    objects = MongoDBManager()

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
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
