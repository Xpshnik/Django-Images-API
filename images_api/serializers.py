from rest_framework import serializers
from .models import UploadedImage, Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thumbnail
        fields = ['height', 'thumbnail']


class ImageSerializer(serializers.ModelSerializer):

    thumbnails = ThumbnailSerializer(read_only=True, many=True)

    class Meta:
        model = UploadedImage
        fields = ['thumbnails', 'fullsize_image']
