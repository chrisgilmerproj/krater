from mongonaut.sites import MongoAdmin
from mongoengine.django.auth import User

from apps.accounts.models import UserSocialAuth

User.mongoadmin = MongoAdmin()
UserSocialAuth.mongoadmin = MongoAdmin()
