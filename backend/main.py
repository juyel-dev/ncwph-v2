from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import cv2
import numpy as np
from ncwph.protocol import NCWPHProtocol

app = FastAPI(
    title="NCWPH v2.0",
    description="Neural Context Wavelet Phase Hashing - Advanced Face Recognition System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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

# ===================== ROOT PAGE =====================
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>NCWPH v2.0</title>
            <style>
                body {
                    font-family: 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    text-align: center;
                    padding: 100px 20px;
                    margin: 0;
                }
                .card {
                    max-width: 700px;
                    margin: 0 auto;
                    background: rgba(255,255,255,0.1);
                    backdrop-filter: blur(10px);
                    padding: 40px;
                    border-radius: 20px;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                h1 { font-size: 3.5rem; margin-bottom: 10px; }
                a { color: #fff; text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>NCWPH v2.0</h1>
                <p style="font-size:1.3rem; opacity:0.9;">Advanced Perceptual Image Hashing & Face Recognition System</p>
                <br>
                <p><strong>Production Deployed on Render.com</strong></p>
                <br>
                <a href="/docs" style="font-size:1.4rem; background:#fff; color:#333; padding:12px 30px; border-radius:50px; text-decoration:none; display:inline-block;">
                    → Open API Documentation
                </a>
                <br><br>
                <p style="opacity:0.7;">Try <code>/health</code> | Enroll & Verify endpoints ready</p>
            </div>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "healthy", "system": "NCWPH v2.0 - Production Ready"}

# Enroll & Verify endpoints (আগের মতোই)
@app.post("/enroll/{user_id}", response_model=ResponseModel)
async def enroll(user_id: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
            
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
            raise HTTPException(status_code=400, detail="Invalid image file")
            
        result = ncwph.verify(image, user_id)
        return {
            "status": "success",
            "message": "Verification completed",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
