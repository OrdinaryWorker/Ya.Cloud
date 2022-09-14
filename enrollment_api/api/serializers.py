from .models import File
from rest_framework import serializers
from django.db import models


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'url', 'size', 'updateDate', 'type', 'parentId')

