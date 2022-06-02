import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from accounts.models import UserAccount
from .validators import validate_is_png_or_jpg


def upload_to(instance, filename):
    if isinstance(instance, UploadedImage):
        return f'images/user_{instance.owner_id:05}/fullsize/{filename}'
    elif isinstance(instance, Thumbnail):
        return f'images/user_{instance.original_image.owner_id:05}/thumbnail_{instance.height}px/{filename}'


class UploadedImage(models.Model):
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    fullsize_image = models.ImageField(upload_to=upload_to, validators=[validate_is_png_or_jpg])

    def make_thumbnail(self, thumbnail_height):
        with Image.open(self.fullsize_image.file.file) as img:
            blob = BytesIO()
            format = img.format
            img = img.copy()
            img.thumbnail((self.fullsize_image.width, thumbnail_height), Image.LANCZOS)
            img.save(blob, format=format)
            blob.seek(0)
            size = sys.getsizeof(blob)
            img = InMemoryUploadedFile(blob, 'ImageField', self.fullsize_image.name, self.fullsize_image.file.content_type, size, None)
            thumbnail_obj = Thumbnail(thumbnail=img)
            return thumbnail_obj.thumbnail


class Thumbnail(models.Model):
    original_image = models.ForeignKey('UploadedImage', related_name='thumbnails', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=upload_to)
    height = models.IntegerField()

    def __str__(self):
        return f'{self.height}px_thumbnail'
