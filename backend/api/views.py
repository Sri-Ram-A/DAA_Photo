from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from . import serializers
from . import models
from . import preprocess
from rq import Queue
from redis import Redis
import os
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Posts
from .serializers import PostSerializer
from rq import Queue
from redis import Redis
import os
import logging

# Redis connection
redis_conn = Redis(host='redis', port=6379, db=0)
grayscale_queue = Queue('grayscale', connection=redis_conn)
resolution_queue = Queue('resolution', connection=redis_conn)
logger = logging.getLogger(__name__)

class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello To My project")

class CreatePost(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        images = models.Posts.objects.all()
        serializer = serializers.PostsSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        logger.debug(f"Received POST data: {request.data}")
        
        serializer = serializers.PostsSerializer(data=request.data)
        if serializer.is_valid():
            # Get process_type before saving
            process_type = request.data.get('process_type')
            
            # Validate process_type
            if process_type not in ['grayscale', 'resolution']:
                return Response(
                    {"error": "Invalid process_type. Must be 'grayscale' or 'resolution'"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save the instance
            instance = serializer.save()
            uploaded_file = request.FILES['image_url']

            try:
                # Save the file to the shared volume for worker processing
                file_path = os.path.join('/shared/uploads', uploaded_file.name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    uploaded_file.seek(0)
                    f.write(uploaded_file.read())

                # Generate pHash
                uploaded_file.seek(0)
                file_bytes = uploaded_file.read()
                pHash = preprocess.generate_phash(file_bytes)
                instance.phash = pHash
                instance.save()

                # Enqueue the task to the appropriate queue
                if process_type == 'grayscale':
                    grayscale_queue.enqueue('worker.process_image', file_path, process_type)
                elif process_type == 'resolution':
                    resolution_queue.enqueue('worker.process_image', file_path, process_type)

                logger.info(f"Successfully queued {process_type} processing for {file_path}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error processing upload: {e}")
                instance.delete()  # Clean up if processing fails
                return Response(
                    {"error": "Failed to process upload"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Alternative simplified view - you can use this instead of CreatePost if you prefer
class ImageUploadView(APIView):
      def post(self, request):
          logger.debug(f"Received POST data: {request.data}")
          serializer = PostSerializer(data=request.data)
          if serializer.is_valid():
              post = serializer.save()
              redis_conn = Redis(host='redis', port=6379, db=0)
              queue = Queue(post.process_type, connection=redis_conn)
              queue.enqueue('worker.process_image', post.image_url.path, post.process_type)
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          logger.error(f"Serializer errors: {serializer.errors}")
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      def get(self, request):
          posts = Posts.objects.all()
          serializer = PostSerializer(posts, many=True)
          return Response(serializer.data, status=status.HTTP_200_OK)
      parser_classes = [MultiPartParser, FormParser]
        
      def get(self, request):
            """Get all images"""
            try:
                images = models.Posts.objects.all()
                serializer = serializers.PostSerializer(images, many=True, context={'request': request})
                print(serializer.data)  # Debugging line to check data
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error fetching images: {e}")
                return Response({"error": "Failed to fetch images"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
      def post(self, request):
            logger.debug(f"Received POST data: {request.data}")
            
            serializer = serializers.PostSerializer(data=request.data)
            if serializer.is_valid():
                post = serializer.save()
                uploaded_file = request.FILES['image_url']
                
                try:
                    # Save file to shared volume for worker processing (same as CreatePost)
                    file_path = os.path.join('/shared/uploads', uploaded_file.name)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    # Write file to shared volume
                    with open(file_path, 'wb') as f:
                        uploaded_file.seek(0)
                        f.write(uploaded_file.read())

                    # Generate pHash
                    uploaded_file.seek(0)
                    file_bytes = uploaded_file.read()
                    pHash = preprocess.generate_phash(file_bytes)
                    post.phash = pHash
                    post.save()
                    
                    # Get the correct queue based on process_type
                    queue_name = post.process_type
                    queue = Queue(queue_name, connection=redis_conn)
                    
                    # Use the shared volume path for worker processing
                    queue.enqueue('worker.process_image', file_path, post.process_type)
                    logger.info(f"Queued {post.process_type} processing for {file_path}")
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    logger.error(f"Error queuing task: {e}")
                    post.delete()  # Clean up if processing fails
                    return Response(
                        {"error": "Failed to queue processing task"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)