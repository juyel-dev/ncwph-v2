from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

class ResponseModel(BaseModel):
    status: str
    message: str
    confidence: float = 0.0
    match: bool = False
    decision: str = ""
    hash: str = ""

@app.get("/health")
def health():
    return {"status": "healthy", "system": "NCWPH v2.0 Production Ready"}

@app.post("/enroll/{user_id}", response_model=ResponseModel)
async def enroll(user_id: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image")
            
        result = ncwph.enroll(image, user_id)
        return {
            "status": "success",
            "message": f"User {user_id} enrolled successfully",
            "hash": result.get("hash", ""),
            "match": True,
            "confidence": 1.0,
            "decision": "ENROLLED"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify/{user_id}", response_model=ResponseModel)
async def verify(user_id: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image")
            
        result = ncwph.verify(image, user_id)
        return {
            "status": "success",
            "message": "Verification completed",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
