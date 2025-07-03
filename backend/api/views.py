from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import HttpResponse
from processing import preprocess
from . import serializers,models
import cv2
import numpy as np
import json
# Create your views here.
class HelloWorld(APIView):
    def get(self,request):
        return Response("Hello To My project")

class CreatePost(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        if pk:
            try:
                post = models.Posts.objects.get(pk=pk)
                meta=json.loads(post.meta)
                print(meta.keys())
                image=preprocess.image_decoding(**meta)
                success, encoded_image = cv2.imencode('.jpg', image)
                if not success:
                    raise ValueError("Failed to encode image")
                return HttpResponse(encoded_image.tobytes(), content_type="image/jpeg")

            except models.Posts.DoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            # serializer = serializers.PostsSerializer(post, context={'request': request})
            # return Response(serializer.data)
        else:
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
            #  Convert bytes to numpy array
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("OpenCV failed to decode image")
            # niw generate hash
            pHash = preprocess.generate_phash(img)
            instance.phash = pHash
            print("Generated pHash:",pHash)
            #niw generate cts and bitstreams
            encoded_dict=preprocess.image_encoding(img)
            instance.meta=json.dumps(encoded_dict)
            
            if instance.processing_type == "grayscale":
                print("Do grayscale things")
            elif instance.processing_type == "resolution":
                print("Do resolution enhancement")
            else:
                print("No extra processing")
            
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
