from django.db import models
from django.contrib.auth.models import User
from accounts.validators import JSONSchemaValidator


THUMBNAIL_HEIGHTS_SCHEMA = {
                 "type": "array",
                 "items": {
                      "type": "integer",
                    },
                 "minItems": 0,
                 "maxItems": 10,
                 "uniqueItems": True
                 }


class AccountTier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    thumbnail_heights = models.JSONField(
        default=list,
        blank=True,
        validators=[JSONSchemaValidator(limit_value=THUMBNAIL_HEIGHTS_SCHEMA)],
        help_text = "Expected format: [200, 400, 600]. As a result three thumbnails with heights 200px, 400px and 600px will be created."
        )
    has_original_link = models.BooleanField(default=False)
    has_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_thumbnails_or_original_or_both",
                check=(
                    models.Q(thumbnail_heights__regex=r'^\[.+\]$', has_original_link=True)
                    | models.Q(thumbnail_heights__regex=r'^\[.+\]$', has_original_link=False)
                    | models.Q(thumbnail_heights__regex=r'^\[\]', has_original_link=True)
                ),
            )
        ]


def get_basic_account_tier():
    return AccountTier.objects.get_or_create(name='Basic', thumbnail_heights=[200])[0]


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tier = models.ForeignKey('AccountTier', related_name='tier_subscribers', blank=False, on_delete=models.SET(get_basic_account_tier))

    def __str__(self):
        return self.user.username
