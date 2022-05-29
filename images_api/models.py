from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #I may end up using customized User model here, so possibly change later
    fullsize_image = models.ImageField(
        upload_to=f'images/user_{owner}/fullsize/%Y/%m/%d',    #TIL {owner:05} doesn't work here
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
        )


""" class Thumbnail(models.Model):
    original_image = models.ForeignKey('Image', related_name='thumbnails' on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=None, height_field=None)
    height = models.IntegerField() """

    #validate if height is less than the original?
