from datetime import timedelta

from django.conf import settings
import mongoengine
from mongoengine.django.auth import User
from mongoengine.queryset import DoesNotExist


class UserSocialAuth(mongoengine.Document):
    """
    Social Auth association model

    This model is used to override UserSocialAuth model
    in django-social-auth
    """
    user = mongoengine.ReferenceField(User)
    provider = mongoengine.StringField(unique_with='uid')
    uid = mongoengine.IntField(unique=True)
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
            name = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')
            try:
                return timedelta(seconds=int(self.extra_data.get(name)))
            except (ValueError, TypeError):
                pass
        return None

setattr(UserSocialAuth, 'DoesNotExist', DoesNotExist)


class Nonce(mongoengine.Document):
    """One use numbers"""
    server_url = mongoengine.StringField()
    timestamp = mongoengine.IntField()
    salt = mongoengine.StringField()

    def __unicode__(self):
        """Unicode representation"""
        return self.server_url


class Association(mongoengine.Document):
    """OpenId account association"""
    server_url = mongoengine.StringField()
    handle = mongoengine.StringField()
    secret = mongoengine.StringField()  # Stored base64 encoded
    issued = mongoengine.IntField()
    lifetime = mongoengine.IntField()
    assoc_type = mongoengine.StringField()

    def __unicode__(self):
        """Unicode representation"""
        return '%s %s' % (self.handle, self.issued)
