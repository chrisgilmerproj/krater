from mongonaut.sites import MongoAdmin

from apps.krater.models import Variety, Vineyard, Wine

Variety.mongoadmin = MongoAdmin()
Vineyard.mongoadmin = MongoAdmin()
Wine.mongoadmin = MongoAdmin()
