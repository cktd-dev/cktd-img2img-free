from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import base64
import json
import time
import io
from PIL import Image

app = FastAPI(title="CKTD FREE Img2Img")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

COMFY_URL = "http://localhost:8188"

@app.get("/")
async def root():
    return {"status": "Img2Img API LIVE", "comfy": COMFY_URL, "docs": "/docs"}

@app.post("/img2img")
async def img2img(ref_image: UploadFile = File(...), prompt: str = Form(...)):
    try:
        img_bytes = await ref_image.read()
        
        workflow = {
            "3": {"inputs
