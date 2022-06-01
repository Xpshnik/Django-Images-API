import os
from django.core.exceptions import ValidationError

def validate_is_png_or_jpg(file):
    valid_file_extensions = ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.png']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError(f'File extension “{ext}” is not allowed. Only jpg and png files supported.')
    valid_mime_types = ['image/png', 'image/jpeg']
    file_mime_type = file.content_type
    if file_mime_type not in valid_mime_types:
        raise ValidationError(f'Unsupported file type ({file_mime_type}). Only jpg and png files supported.')
