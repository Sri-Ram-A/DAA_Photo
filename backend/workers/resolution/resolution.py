from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import time, random
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/process/resolution")
async def upscale_image(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    upscale = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    time.sleep(random.randint(10, 30))  # Simulated delay
    _, img_encoded = cv2.imencode('.jpg', upscale)
    return StreamingResponse(BytesIO(img_encoded.tobytes()), media_type="image/jpeg")