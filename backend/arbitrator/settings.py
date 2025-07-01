from pathlib import Path
import os

   # Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

   # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lwd_w04h*n258^29#xvaj6d-v6@3x89n5vit0%u30xpr=(34js'

   # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # Adjust for production
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
   # Application definition
INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'rest_framework',
       'api',
       'corsheaders',
       'django_minio_backend',
   ]

MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'corsheaders.middleware.CorsMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
   ]

ROOT_URLCONF = 'arbitrator.urls'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]

WSGI_APPLICATION = 'arbitrator.wsgi.application'

   # Database
DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }

   # Password validation
AUTH_PASSWORD_VALIDATORS = [
       {
           'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
       },
       {
           'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
       },
       {
           'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
       },
       {
           'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
       },
   ]

   # Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

  # Static and media files
STATIC_URL = '/static/'
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

   # Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

   # MinIO Configuration
# USE_MINIO = os.environ.get('USE_MINIO', 'False') == 'True'
USE_MINIO=True
if USE_MINIO:
       STORAGES = {
           "default": {
               "BACKEND": "django_minio_backend.models.MinioBackend",
               "OPTIONS": {
                   "bucket_name": os.environ.get('MINIO_BUCKET_NAME', 'django-backend-dev'),
               },
           },
           "staticfiles": {
               "BACKEND": "django_minio_backend.models.MinioBackendStatic",
               "OPTIONS": {
                   "bucket_name": os.environ.get('MINIO_STATIC_FILES_BUCKET', 'static'),
               },
           },
       }
       MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'localhost:9000')
       MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
       MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
       MINIO_PUBLIC_BUCKETS = [
           os.environ.get('MINIO_BUCKET_NAME', 'django-backend-dev'),
           os.environ.get('MINIO_STATIC_FILES_BUCKET', 'static'),
       ]
       MINIO_PRIVATE_BUCKETS = []
       MINIO_MEDIA_FILES_BUCKET = os.environ.get('MINIO_BUCKET_NAME', 'django-backend-dev')
       MINIO_STATIC_FILES_BUCKET = os.environ.get('MINIO_STATIC_FILES_BUCKET', 'static')
       MINIO_USE_HTTPS = False
       MINIO_BUCKET_CHECK_ON_SAVE = False  # Disable bucket check for local development
       MINIO_CONSISTENCY_CHECK_ON_START = False  # Disable consistency check
else:
       # Fallback to filesystem storage
       MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))