from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AccountTier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    thumbnail_heights = models.JSONField()
    has_original_link = models.BooleanField(default=False)
    has_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey('AccountTier', related_name='tier_subscribers', on_delete=models.CASCADE) #change CASCADE to sth more appropriate later

    def __str__(self):
        return self.user.username
