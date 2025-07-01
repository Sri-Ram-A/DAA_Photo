from rest_framework import serializers
from . import models
class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Posts
        fields="__all__"