from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime
from minio import Minio

from . import serializers, models, preprocess, worker_queue


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello To My project")


class CreatePost(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Return all uploaded images.
        """
        posts = models.Posts.objects.all().order_by('-id')
        serializer = serializers.PostsSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Upload and optionally process an image.
        """
        processing_type = request.data.get("processing_type", "none")
        uploaded_file = request.FILES.get('image_url')

        if not uploaded_file:
            return Response({"error": "No image uploaded"}, status=400)

        file_bytes = uploaded_file.read()

        # Process image if needed
        if processing_type != "none":
            processed, result = worker_queue.send_to_worker(processing_type, file_bytes, uploaded_file.name)
            if not processed:
                return Response({"error": f"Processing failed: {result}"}, status=500)
            file_bytes = processed
            worker_queue.release_worker(processing_type, result)

        # Generate pHash
        pHash = preprocess.generate_phash(file_bytes)

        # Check for duplicates
        duplicates = models.Posts.objects.filter(phash=pHash)
        duplicate_group = 1 if not duplicates.exists() else 2

        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        original_name = uploaded_file.name.rsplit('.', 1)[0]
        extension = uploaded_file.name.rsplit('.', 1)[-1]
        new_filename = f"{original_name}_{processing_type}_{timestamp}.{extension}"

        # Save image to MinIO
        image_field = ContentFile(file_bytes)
        image_field.name = new_filename

        # Save Post in DB
        post = models.Posts.objects.create(
            creator=request.data.get("creator"),
            title=request.data.get("title"),
            description=request.data.get("description"),
            image_url=image_field,
            phash=pHash,
            processing_type=processing_type,
            duplicate_group=duplicate_group
        )

        serializer = serializers.PostsSerializer(post)
        return Response(serializer.data, status=201)


class ClearAllData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):  # Temporary GET support for browser access
        return self.delete(request)

    def delete(self, request):
        if not settings.USE_MINIO:
            return Response({"error": "MinIO not enabled"}, status=400)

        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_HTTPS
        )

        bucket = settings.MINIO_MEDIA_FILES_BUCKET

        try:
            objects = client.list_objects(bucket, recursive=True)
            delete_objects = [obj.object_name for obj in objects]

            if delete_objects:
                client.remove_objects(bucket, delete_objects)

            models.Posts.objects.all().delete()

            return Response(
                {"message": f"✅ Cleared {len(delete_objects)} MinIO files and all DB posts."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
