from django.db import models

from ..simple_identifier import SimpleUniqueIdentifier, SimpleTimestampIdentifier


class Identifier(SimpleUniqueIdentifier):
    random_string_length = 2
    template = '{device_id}{timestamp}{random_string}'
    identifier_cls = SimpleTimestampIdentifier


class TrackingIdentifierModelMixin(models.Model):

    """A model mixin to add a traking identifier.
    """

    tracking_identifier_cls = Identifier
    tracking_identifier_prefix = ''

    tracking_identifier = models.CharField(
        max_length=25,
        unique=True)

    def __str__(self):
        return f'{self.tracking_identifier[-9:]}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.tracking_identifier = self.tracking_identifier_cls(
                identifier_prefix=self.tracking_identifier_prefix,
                identifier_type=self._meta.label_lower
            ).identifier
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.tracking_identifier, )

    @property
    def identifier(self):
        """Returns a shortened tracking identifier.
        """
        return self.tracking_identifier[-9:]

    class Meta:
        abstract = True
