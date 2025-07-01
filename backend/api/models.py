from django.db import models
from django_minio_backend import MinioBackend
import os

def upload_to(instance, filename):
    """Generate upload path for images."""
    return f"images/{filename}"

class Posts(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.ImageField(
        storage=MinioBackend(bucket_name=os.environ.get('MINIO_BUCKET_NAME', 'django-backend-dev')) if os.environ.get('USE_MINIO', 'False') == 'True' else None,
        upload_to=upload_to,
        blank=True,
        null=True
    )
    process_type = models.CharField(
        max_length=20,
        choices=[('grayscale', 'Grayscale'), ('resolution', 'Resolution')],
        default='grayscale'
    )
    phash = models.CharField(max_length=64, blank=True, null=True)
    processed_image_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled"

    def get_image_url(self):
        """Return public URL for the image."""
        if os.environ.get('USE_MINIO', 'False') == 'True' and self.image_url:
            return f"http://localhost:9000/{os.environ.get('MINIO_BUCKET_NAME', 'django-backend-dev')}/{self.image_url.name}"
        return self.image_url.url if self.image_url else ""