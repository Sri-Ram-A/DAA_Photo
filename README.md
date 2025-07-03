# photo_daa
DAA project for 4th semester
#to run the docker image of database
docker run --name "MiniIODatabase" -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ":9001"

if u get this error or any error similar,delete backend/migrations folder and migrate again 
django_minio_backend.utils.ConfigurationError: The configured bucket (media) must be declared either in MINIO_PRIVATE_BUCKETS or MINIO_PUBLIC_BUCKETS
field=models.ImageField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='media', replace_existing=True), upload_to=api.models.upload_to),

python manage.py makemigrations api


https://www.docker.com/blog/how-to-dockerize-django-app/
You can build the Django Docker container with the following command:

    'corsheaders',###https://pypi.org/project/django-cors-headers/
    'django_minio_backend',###https://pypi.org/project/django-minio-backend/
    # if you remove above line,inspite of running minio server,it will not work


1
docker build -t django-docker .
To see your image, you can run:

1
docker image list
The result will look something like this:

1
2
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
django-docker   latest    ace73d650ac6   20 s
https://medium.com/@michal.drozdze/how-to-reduce-the-size-of-your-docker-image-and-build-time-by-90-23a303a54c66 ->I USED 


