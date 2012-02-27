from mongonaut.sites import MongoAdmin
from mongoengine.django.auth import User

from apps.accounts.models import UserSocialAuth
from apps.krater.mongoadmin import NewAdmin as MongoAdmin

User.mongoadmin = MongoAdmin()
UserSocialAuth.mongoadmin = MongoAdmin()
