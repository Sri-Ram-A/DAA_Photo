from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import HttpResponse,FileResponse
from django.apps import apps
tree = apps.get_app_config("api").tree
import cv2
import numpy as np
import json

from processing import preprocess
from . import serializers,models



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

        else:
            images = models.Posts.objects.all()
            serializer = serializers.PostsSerializer(images, many=True, context={'request': request})
            return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PostsSerializer(data=request.data) #reuqest.data is a django QueryDict
        # <QueryDict: {'title': ['etag'], 'description': ['Electric Guitar'], 'creator': ['electric wizard'],
        # 'processing_type': ['resolution'], 'image_url': [<InMemoryUploadedFile: Screenshot 2025-05-24 113022.png (image/png)>]}>
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
            key = tree.search(pHash)
            if key == None:
                print(f"🔍 Key {pHash} not found in tree.")
                #now store in tree 
                meta_dict = {
                "pHash": pHash,
                "title": instance.title,
                "description": instance.description,
                "creator": instance.creator,
                "uploaded_at": instance.uploaded_at.isoformat(),  # 💡 convert datetime to string!
                "processing_type": instance.processing_type,
                }
                tree.insert(pHash, meta_dict)
                preprocess.save_tree(tree)
                

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
            else:
                instance.delete()
                print(f"‼️ Key {pHash} already found in tree.")
                return Response({"error":"image existing"},status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VisualizeTreeDatabase(APIView):
    def get(self,request):
        filename=tree.visualize()
        
        # Open the PDF file in binary mode
        file_handle = open(filename, 'rb')
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="tree_visualization.pdf"'
        return response