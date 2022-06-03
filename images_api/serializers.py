from collections import OrderedDict
from rest_framework import serializers
from .models import UploadedImage, Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thumbnail
        fields = ['height', 'thumbnail']


class ImageSerializer(serializers.ModelSerializer):

    thumbnails = ThumbnailSerializer(read_only=True, many=True)
    user = serializers.ReadOnlyField(source='owner.user.username')

    class Meta:
        model = UploadedImage
        fields = ['user', 'fullsize_image', 'thumbnails']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        #when there're thumbnails of wrong heights due to cases when AccountTier values were edited or tier for user was changed
        #TODO: implement automatic delete/creation of wrong thumbnail heights for the described above cases instead of checking and filtering here
        expected_heights = set(instance.owner.tier.thumbnail_heights)
        received_heights = {thumb['height'] for key in result for thumb in result[key] if key=='thumbnails'}
        redundant_heights = received_heights - expected_heights
        missing_heights = expected_heights - received_heights
        if redundant_heights:
            result['thumbnails'] = [
                thumbnail for key in result for thumbnail in result[key]
                if key=='thumbnails' if thumbnail['height'] in expected_heights
                ]
        if missing_heights:
            result['thumbnails'] += ['Seems like changes happened to your account tier, but the thumbnail links weren\'t updated']
        if not self.context['request'].user.useraccount.tier.has_original_link:
            del result['fullsize_image']
        return OrderedDict((key, result[key]) for key in result if result[key]) or 'Unlock this item with subscriptions that provide original sized images.'
