from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
import io
from PIL import Image
import os
import uvicorn

app = FastAPI(title="CKTD FREE Img2Img")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ComfyUI server (internal)
os.system("cd ComfyUI && python main.py --listen 0.0.0.0 --port 8188 &")
COMFY_URL = "http://localhost:8188"

@app.get("/")
async def root():
    return {"api": "Img2Img LIVE", "port": COMFY_URL}

@app.post("/img2img")
async def img2
