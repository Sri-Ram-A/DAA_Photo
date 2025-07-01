from rest_framework import serializers
from .models import Posts

class PostSerializer(serializers.ModelSerializer):
      image_url = serializers.ImageField(required=True)
      title = serializers.CharField(required=False, allow_blank=True)
      description = serializers.CharField(required=False, allow_blank=True)
      process_type = serializers.ChoiceField(choices=[('grayscale', 'Grayscale'), ('resolution', 'Resolution')], required=True)
      public_image_url = serializers.SerializerMethodField()
      creator = serializers.IntegerField(source='creator.id', read_only=True, default=1)  # Adjust based on your auth model

      class Meta:
          model = Posts
          fields = ['id', 'title', 'description', 'image_url', 'process_type', 'phash', 'public_image_url', 'processed_image_url', 'creator']

      def get_public_image_url(self, obj):
          return obj.get_image_url()