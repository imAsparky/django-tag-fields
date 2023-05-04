from rest_framework import serializers

from tag_fields.serializers import TagSerializer, TagListSerializerField

from .models import TestModel


class TestModelSerializer(TagSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = TestModel
        fields = "__all__"
