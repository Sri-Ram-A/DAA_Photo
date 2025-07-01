import os
import time
import random
from PIL import Image
from rq import Queue, Worker
from redis import Redis
from minio import Minio

def process_image(file_path, process_type):
    use_minio = os.environ.get('USE_MINIO', 'False') == 'True'
    output_folder = f"/shared/processed/{process_type}"
    log_file = f"/shared/processed/{process_type}_times.log"
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(file_path)
    output_path = os.path.join(output_folder, filename)

    if os.path.exists(output_path):
        return

    print(f"[Worker] Processing {process_type}: {filename}")
    start = time.time()
    time.sleep(random.randint(5, 10))  # Simulate processing time
    img = Image.open(file_path)

    if process_type == 'grayscale':
        img = img.convert("L")
    elif process_type == 'resolution':
        img = img.resize((img.width * 2, img.height * 2))

    img.save(output_path)
    end = time.time()

    if use_minio:
        minio_client = Minio(
            os.environ.get('MINIO_ENDPOINT', 'minio:9000'),
            access_key=os.environ.get('MINIO_ACCESS_KEY', 'minioadmin'),
            secret_key=os.environ.get('MINIO_SECRET_KEY', 'minioadmin'),
            secure=False
        )
        bucket_name = os.environ.get('MINIO_BUCKET_NAME', 'django-backend-dev')
        minio_client.fput_object(bucket_name, f"processed/{process_type}/{filename}", output_path)

    with open(log_file, "a") as f:
        f.write(f"{process_type},{filename},{end - start:.2f}\n")

if __name__ == '__main__':
    redis_conn = Redis(host='redis', port=6379, db=0)
    queue_name = os.environ.get('QUEUE_NAME', 'grayscale')
    queue = Queue(queue_name, connection=redis_conn)
    worker = Worker([queue], connection=redis_conn)
    worker.work()