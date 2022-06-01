from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UploadedImage, Thumbnail

#when creating or updating objects in bulk, none of save(), pre_save, and post_save is called, 
#so UploadedImage.objects.bulk_create() anywhere in this project would result in a bug with thumbnails not created
@receiver(pre_save, sender=UploadedImage)
def make_thumbnails(sender, instance, **kwargs):
    if instance.pk is None:
        instance._thumbnail_drafts = [
            instance.make_thumbnail(thumb_height)
            for thumb_height in instance.owner.tier.thumbnail_heights
            if thumb_height < instance.fullsize_image.height
        ]
    """instance.owner.tier or instance.owner.tier.thumbnail_heights changed? """


@receiver(post_save, sender=UploadedImage)
def initiate_thumbnails(sender, instance, created, **kwargs):
    if created:
        instance.thumbnails.set(
            Thumbnail.objects.bulk_create([
                Thumbnail(original_image=instance, thumbnail=thumbnail, height=thumbnail.height)
                for thumbnail in instance._thumbnail_drafts
        ]))
