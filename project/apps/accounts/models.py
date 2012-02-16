from datetime import timedelta

from django.conf import settings
import mongoengine
from mongoengine.django.auth import User


class UserSocialAuth(mongoengine.Document):
    """
    Social Auth association model

    This model is used to override UserSocialAuth model
    in django-social-auth
    """
    user = mongoengine.ReferenceField(User)
    provider = mongoengine.StringField(unique_with='uid')
    uid = mongoengine.StringField(unique=True)
    extra_data = mongoengine.DictField()

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')

    def __unicode__(self):
        """Return associated user unicode representation"""
        return unicode(self.user)

    def expiration_delta(self):
        """Return saved session expiration seconds if any. Is retuned in
        the form of a timedelta data type. None is returned if there's no
        value stored or it's malformed.
        """
        if self.extra_data:
            name = settings.get('SOCIAL_AUTH_EXPIRATION', 'expires')
            try:
                return timedelta(seconds=int(self.extra_data.get(name)))
            except (ValueError, TypeError):
                pass
        return None
