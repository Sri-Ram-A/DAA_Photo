from django.apps import AppConfig
from django_minio_backend import MinioBackend ###

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    ### BELOW ADDED BY ME
    def ready(self):
        minio = MinioBackend()
        result = minio.is_minio_available()
        if result:
            print("✅ MinIO is available.")
        else:
            print("❌ MinIO is not available. Using File system storage")
            print(result.details)