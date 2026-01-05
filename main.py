import base64
import json
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import requests
import uuid
import time

app = FastAPI(title="CKTD FREE Img2Img API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

COMFY_URL = "http://localhost:8188/prompt"

@app.get("/")
async def root():
    return {"api": "CKTD FREE Img2Img (Ref+Prompt)", "docs": "/docs"}

@app.post("/img2img")
async def img2img(ref_image: UploadFile = File(...), prompt: str = Form(...), strength: float = Form(0.7)):
    try:
        # Load workflow
        with open("workflow_img2img.json") as f:
            workflow = json.load(f)
        
        # Update workflow
        workflow["6"]["inputs"]["image"] = encode_image(await ref_image.read())
        workflow["5"]["inputs"]["text"] = prompt
        workflow["7"]["inputs"]["strength"] = strength
        
        # Queue
        resp = requests.post(COMFY_URL, json={"prompt": workflow})
        prompt_id = resp.json()["prompt_id"]
        
        # Wait & get image
        for _ in range(120):  # 2 min timeout
            time.sleep(1)
            history = requests.get(f"http://localhost:8188/history/{prompt_id}").json()
            if prompt_id in history:
                images = history[prompt_id]["outputs"]["13"]["images"][0]
                img_data = requests.get(f"http://localhost:8188/view?filename={images['filename']}").content
                img_b64 = base64.b64encode(img_data).decode()
                return {"image": f"data:image/png;base64,{img_b64}"}
        
        return JSONResponse(status_code=408, content={"error": "Timeout"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def encode_image(image_bytes):
    from base64 import b64encode
    buffer = io.BytesIO(image_bytes)
    img = Image.open(buffer)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return {"filename": f"input.png", "data": b64encode(buffer.getvalue()).decode()}
