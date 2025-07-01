from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from . import serializers,models,preprocess

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
            instance=serializer.save()
            uploaded_file = request.FILES['image_url'] # Just extracts image name 
            uploaded_file.seek(0)
            file_bytes = uploaded_file.read()  # Read into memory
            # Generate pHash without saving to disk
            pHash = preprocess.generate_phash(file_bytes)
            instance.phash = pHash
            print("Generated pHash:",pHash)
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
