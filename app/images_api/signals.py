import binascii
from io import BytesIO
from celery import group
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UploadedImage, Thumbnail
from .tasks import make_thumbnail

#when creating or updating objects in bulk, none of save(), pre_save, and post_save is called, 
#so UploadedImage.objects.bulk_create() anywhere in this project would result in a bug with thumbnails not created
@receiver(pre_save, sender=UploadedImage)
def make_thumbnails(sender, instance, **kwargs):
    if instance.pk is None:
        name = instance.fullsize_image.name
        content_type = instance.fullsize_image.file.content_type
        serialized_fullsize_image_blob = binascii.b2a_base64(instance.fullsize_image.file.file.getvalue()).decode('utf8')
        jobs = group([
            make_thumbnail.s(serialized_fullsize_image_blob, thumb_height, name, content_type)
            for thumb_height in instance.owner.tier.thumbnail_heights
            if thumb_height < instance.fullsize_image.height
        ])
        instance._thumbnail_drafts = jobs.apply_async()


@receiver(post_save, sender=UploadedImage)
def initiate_thumbnails(sender, instance, created, **kwargs):
    if created:
        instance.thumbnails.set(
            Thumbnail.objects.bulk_create([
                Thumbnail(
                    original_image=instance,
                    thumbnail=InMemoryUploadedFile(BytesIO(binascii.a2b_base64(serialized_blob.encode('utf8'))), *metadata),
                    height=thumbnail_height
                )
                for serialized_blob, thumbnail_height, *metadata in instance._thumbnail_drafts.get()
        ]))
