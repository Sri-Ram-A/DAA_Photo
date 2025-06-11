import boto3
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render


s3 = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
)

BUCKET_NAME = 'mybucket'

def upload_files(request):
    if request.method == 'POST':
        try:
            print("creating bucket")
            s3.create_bucket(Bucket=BUCKET_NAME)
        except s3.exceptions.BucketAlreadyOwnedByYou:
            pass  

        for file in request.FILES.getlist('files'):
            s3.upload_fileobj(file, BUCKET_NAME, file.name)
        return HttpResponse("Files uploaded to MinIO")
    return render(request, 'minio_handler/upload.html')

def list_files(request):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = [obj['Key'] for obj in response.get('Contents', [])]
    except Exception as e:
        files = []
    return render(request, 'minio_handler/list_files.html', {'files': files})

def download_file(request, filename):
    try:
        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
        file_stream = file_obj['Body']
        return FileResponse(file_stream, as_attachment=True, filename=filename)
    except Exception:
        raise Http404("File not found")
