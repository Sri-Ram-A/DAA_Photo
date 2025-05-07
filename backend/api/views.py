from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from . import serializers
from . import models
# Create your views here.
class HelloWorld(APIView):
    def get(self,request):
        return Response("Hello To My project")
    
class CreatePost(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        images = models.Posts.objects.all()
        serializer = serializers.PostsSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)