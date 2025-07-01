from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import time, random
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/process/grayscale")
async def grayscale_image(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    time.sleep(random.randint(10, 30))  # Simulated delay
    _, img_encoded = cv2.imencode('.jpg', gray)
    return StreamingResponse(BytesIO(img_encoded.tobytes()), media_type="image/jpeg")
