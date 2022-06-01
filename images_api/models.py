from django.db import models
from accounts.models import UserAccount
from .validators import validate_is_png_or_jpg


def upload_to(instance, filename):
    if isinstance(instance, UploadedImage):
        return f'images/user_{instance.owner.pk:05}/fullsize/{filename}'
    elif isinstance(instance, Thumbnail):
        return f'images/user_{instance.original_image.owner.pk:05}/thumbnail_{instance.height}px/{filename}'


class UploadedImage(models.Model):
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    fullsize_image = models.ImageField(upload_to=upload_to, validators=[validate_is_png_or_jpg])

    def make_thumbnail(self, thumbnail_height):
        return self.fullsize_image


class Thumbnail(models.Model):
    original_image = models.ForeignKey('UploadedImage', related_name='thumbnails', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=upload_to)
    height = models.IntegerField()

    def __str__(self):
        return f'{self.height}px_thumbnail'
