import os
import random
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
IMAGE_DIR = r"C:\Users\tjsre\Pictures\Camera Roll"
BASE_URL = "http://localhost:8000"
SERVER_URL = f"{BASE_URL}/api/images/"  # Fixed: Should be /api/images/ not /images/
PROCESSING_TYPES = ["grayscale", "resolution", "none"]
IMAGES_PER_TYPE = 15

# Session for maintaining cookies
session = requests.Session()

def get_csrf_token():
    """Get CSRF token from the server using multiple methods."""
    try:
        print("🔍 Trying method 1: GET request to /images/")
        response = session.get(SERVER_URL)
        print(f"   Status: {response.status_code}")
        csrf_token = session.cookies.get('csrftoken')
        if csrf_token:
            print(f"   ✅ Found CSRF token in cookies: {csrf_token[:20]}...")
            return csrf_token
        print("   ❌ No CSRF token in cookies")
        
        print("🔍 Trying method 2: GET request to root /")
        response = session.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        csrf_token = session.cookies.get('csrftoken')
        if csrf_token:
            print(f"   ✅ Found CSRF token in cookies: {csrf_token[:20]}...")
            return csrf_token
        print("   ❌ No CSRF token in cookies")
        
        print("🔍 Trying method 3: GET request to /api/")
        response = session.get(f"{BASE_URL}/api/")
        print(f"   Status: {response.status_code}")
        csrf_token = session.cookies.get('csrftoken')
        if csrf_token:
            print(f"   ✅ Found CSRF token in cookies: {csrf_token[:20]}...")
            return csrf_token
        print("   ❌ No CSRF token in cookies")
        
        print("🔍 Trying method 4: Extract from HTML content")
        # Try to extract from any HTML response
        for url in [f"{BASE_URL}/", f"{BASE_URL}/api/", SERVER_URL]:
            try:
                response = session.get(url)
                if 'html' in response.headers.get('content-type', '').lower():
                    # Look for CSRF token in HTML
                    csrf_patterns = [
                        r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']',
                        r'csrftoken["\']:\s*["\']([^"\']+)["\']',
                        r'csrf_token["\']:\s*["\']([^"\']+)["\']',
                    ]
                    
                    for pattern in csrf_patterns:
                        csrf_match = re.search(pattern, response.text)
                        if csrf_match:
                            token = csrf_match.group(1)
                            print(f"   ✅ Found CSRF token in HTML: {token[:20]}...")
                            return token
            except:
                continue
        
        print("🔍 Trying method 5: Django admin page")
        try:
            response = session.get(f"{BASE_URL}/admin/")
            csrf_token = session.cookies.get('csrftoken')
            if csrf_token:
                print(f"   ✅ Found CSRF token from admin: {csrf_token[:20]}...")
                return csrf_token
        except:
            pass
            
        print("⚠️ All methods failed to obtain CSRF token")
        print("📋 Available cookies:", dict(session.cookies))
        return None
        
    except Exception as e:
        print(f"❌ Error getting CSRF token: {e}")
        return None

def get_jpg_files(directory):
    """Get all JPG files from the specified directory."""
    jpg_files = []
    try:
        for file in os.listdir(directory):
            if file.lower().endswith(('.jpg', '.jpeg')):
                jpg_files.append(os.path.join(directory, file))
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
    return jpg_files

def send_request(image_path, processing_type, request_id, csrf_token):
    """Send a single POST request to the server with CSRF token."""
    try:
        start_time = time.time()
        
        with open(image_path, 'rb') as f:
            files = {'image_url': f}
            data = {
                'creator': f'DOS_Test_{request_id}',
                'title': f'DOS Attack Image {request_id}',
                'description': f'Testing {processing_type} processing',
                'processing_type': processing_type
            }
            
            headers = {
                'Referer': BASE_URL  # Required for CSRF validation
            }
            
            # Only add CSRF token if we have one
            if csrf_token:
                data['csrfmiddlewaretoken'] = csrf_token
                headers['X-CSRFToken'] = csrf_token
            
            print(f"🚀 [{request_id}] Sending {processing_type} request with {os.path.basename(image_path)}")
            
            response = session.post(SERVER_URL, files=files, data=data, headers=headers, timeout=120)
            
        end_time = time.time()
        duration = end_time - start_time
        
        result = {
            'request_id': request_id,
            'image': os.path.basename(image_path),
            'processing_type': processing_type,
            'status_code': response.status_code,
            'duration': duration,
            'response_size': len(response.content),
            'success': response.status_code == 201
        }
        
        if response.status_code == 201:
            print(f"✅ [{request_id}] SUCCESS - {processing_type} - {duration:.2f}s - {os.path.basename(image_path)}")
        else:
            print(f"❌ [{request_id}] FAILED - {processing_type} - {response.status_code} - {response.text[:100]}")
            result['error'] = response.text[:200]
            
        return result
        
    except requests.exceptions.Timeout:
        print(f"⏰ [{request_id}] TIMEOUT - {processing_type} - {os.path.basename(image_path)}")
        return {
            'request_id': request_id,
            'image': os.path.basename(image_path),
            'processing_type': processing_type,
            'status_code': 'TIMEOUT',
            'duration': 120,
            'success': False,
            'error': 'Request timeout'
        }
    except Exception as e:
        print(f"💥 [{request_id}] ERROR - {processing_type} - {str(e)}")
        return {
            'request_id': request_id,
            'image': os.path.basename(image_path),
            'processing_type': processing_type,
            'status_code': 'ERROR',
            'duration': 0,
            'success': False,
            'error': str(e)
        }

def main():
    print("🔥 Starting DOS Attack on Image Processing Server")
    print("=" * 60)
    
    # Get CSRF token first
    print("🔐 Getting CSRF token...")
    csrf_token = get_csrf_token()
    
    if not csrf_token:
        print("\n⚠️ Could not get CSRF token. Trying without CSRF protection...")
        print("💡 This might work if your API endpoints have @csrf_exempt decorator")
        csrf_token = ""  # Try with empty token
    else:
        print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
    
    # Get all JPG files
    jpg_files = get_jpg_files(IMAGE_DIR)
    
    if len(jpg_files) < 15:
        print(f"⚠️ Warning: Only found {len(jpg_files)} JPG files. Need at least 15.")
        if len(jpg_files) == 0:
            print("❌ No JPG files found. Exiting.")
            return
    
    print(f"📁 Found {len(jpg_files)} JPG files in directory")
    
    # Prepare requests
    requests_to_send = []
    request_id = 1
    
    for processing_type in PROCESSING_TYPES:
        # Select random images for each processing type
        selected_images = random.sample(jpg_files, min(IMAGES_PER_TYPE, len(jpg_files)))
        
        for image_path in selected_images:
            requests_to_send.append((image_path, processing_type, request_id))
            request_id += 1
    
    print(f"🎯 Prepared {len(requests_to_send)} concurrent requests")
    print("📋 Request breakdown:")
    for ptype in PROCESSING_TYPES:
        count = sum(1 for _, pt, _ in requests_to_send if pt == ptype)
        print(f"   - {ptype}: {count} requests")
    
    print("\n🚀 Launching all requests simultaneously...")
    print("=" * 60)
    
    # Launch all requests concurrently
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Submit all requests
        future_to_request = {
            executor.submit(send_request, img_path, proc_type, req_id, csrf_token): (img_path, proc_type, req_id)
            for img_path, proc_type, req_id in requests_to_send
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_request):
            result = future.result()
            results.append(result)
    
    total_time = time.time() - start_time
    
    # Analyze results
    print("\n" + "=" * 60)
    print("📊 ATTACK RESULTS SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"📈 Total Requests: {len(results)}")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"⏱️ Total Attack Duration: {total_time:.2f} seconds")
    print(f"📊 Success Rate: {len(successful)/len(results)*100:.1f}%")
    
    # Breakdown by processing type
    print("\n📋 Results by Processing Type:")
    for ptype in PROCESSING_TYPES:
        type_results = [r for r in results if r['processing_type'] == ptype]
        type_success = [r for r in type_results if r['success']]
        avg_duration = sum(r['duration'] for r in type_results) / len(type_results)
        
        print(f"   {ptype.upper()}:")
        print(f"     - Total: {len(type_results)}")
        print(f"     - Success: {len(type_success)}")
        print(f"     - Avg Duration: {avg_duration:.2f}s")
    
    # Show failed requests
    if failed:
        print(f"\n❌ Failed Requests ({len(failed)}):")
        for result in failed:
            error_msg = result.get('error', 'Unknown error')[:50]
            print(f"   [{result['request_id']}] {result['processing_type']} - {result['status_code']} - {error_msg}")
    
    # Show slowest requests
    print(f"\n⏰ Slowest Requests:")
    slowest = sorted([r for r in results if isinstance(r['duration'], (int, float))], 
                    key=lambda x: x['duration'], reverse=True)[:5]
    for result in slowest:
        print(f"   [{result['request_id']}] {result['processing_type']} - {result['duration']:.2f}s - {result['image']}")
    
    print(f"\n🔥 DOS Attack completed!")

if __name__ == "__main__":
    main()