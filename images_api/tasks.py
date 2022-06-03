import sys
import binascii
from io import BytesIO
from PIL import Image
from celery import shared_task


@shared_task()
def make_thumbnail(serialized_original_image:str, thumbnail_height:int, image_name:str, content_type:str):
    restored_original_image = BytesIO(binascii.a2b_base64(serialized_original_image.encode('utf8')))
    with Image.open(restored_original_image) as img:
        blob = BytesIO()
        format = img.format
        img = img.copy()
        img.thumbnail((img.width, thumbnail_height), Image.LANCZOS)
        img.save(blob, format=format)
        blob.seek(0)
        size = sys.getsizeof(blob)
        serialized_thumbnail_blob = binascii.b2a_base64(blob.getvalue()).decode('utf8')
        return serialized_thumbnail_blob, thumbnail_height, 'ImageField', image_name, content_type, size, None
