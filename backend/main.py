from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ncwph.protocol import NCWPHProtocol

app = FastAPI(title="NCWPH v2.0 - Production API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ncwph = NCWPHProtocol()

@app.post("/enroll/{user_id}")
async def enroll(user_id: str, file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return ncwph.enroll(image, user_id)

@app.post("/verify/{user_id}")
async def verify(user_id: str, file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return ncwph.verify(image, user_id)

@app.get("/health")
def health():
    return {"status": "healthy", "system": "NCWPH v2.0"}
