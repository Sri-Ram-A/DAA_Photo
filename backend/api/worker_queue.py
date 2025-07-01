# api/worker_queue.py
import threading
import requests

# Initial worker pool status
worker_pool = {
    "grayscale": {"8001": "free", "8003": "free"},
    "resolution": {"8002": "free", "8004": "free"}
}

lock = threading.Lock()

def assign_worker(process_type):
    with lock:
        for port, status in worker_pool[process_type].items():
            if status == "free":
                worker_pool[process_type][port] = "busy"
                return port
    return None  # No free worker

def release_worker(process_type, port):
    with lock:
        worker_pool[process_type][port] = "free"
import time

def send_to_worker(process_type, file_bytes, filename):
    port = assign_worker(process_type)
    if not port:
        print(f"[{process_type.upper()}] No free worker available.")
        return None, "No free worker"

    print(f"[{process_type.upper()}]  Assigned worker at port {port} for file '{filename}'")

    start_time = time.time()

    try:
        url = f"http://localhost:{port}/process/{process_type}"
        files = {'file': (filename, file_bytes, 'image/jpeg')}
        res = requests.post(url, files=files, timeout=60)

        end_time = time.time()
        elapsed = round(end_time - start_time, 2)
        print(f"[{process_type.upper()}]  Time taken by worker {port}: {elapsed} seconds")

        if res.status_code == 200:
            return res.content, port
        else:
            print(f"[{process_type.upper()}]  Worker error with status {res.status_code}")
            return None, f"Worker error: {res.status_code}"
    except Exception as e:
        print(f"[{process_type.upper()}] ❌ Exception occurred: {e}")
        return None, str(e)
