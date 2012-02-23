from datetime import timedelta

from django.conf import settings
from django.db.models import signals
import mongoengine
from mongoengine.django.auth import User as MongoUser
from mongoengine.queryset import DoesNotExist


class User(MongoUser):

    def save(self, safe=True, force_insert=False):
        signals.pre_save.send(sender=self.__class__, instance=self)
        before = '_id' in self and self['_id'] or None
        super(User, self).save(safe=safe, force_insert=force_insert)
        after = '_id' in self and self['_id'] or None
        signals.post_save.send(sender=self.__class__, instance=self,
                               created=bool(not before and after))

    def delete(self, safe=False):
        signals.pre_delete.send(sender=self.__class__, instance=self)
        super(User, self).delete(safe=safe)
        signals.post_delete.send(sender=self.__class__, instance=self)


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
            expires = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')
            try:
                return timedelta(seconds=int(self.extra_data.get(expires)))
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
