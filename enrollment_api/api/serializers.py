from .models import File
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist,ValidationError

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'url', 'size', 'date', 'type', 'parentId')

    def create(self, validated_data):
        if validated_data['type'] == 'FOLDER':
            if validated_data.get('url'):
                return None
            if validated_data.get('size'):
                return None

        if validated_data['type'] == 'FILE':
            if not validated_data.get('url') or validated_data.get('size') < 0:
                return None

        file = File.objects.create(**validated_data)
        return file
