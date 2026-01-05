FROM ghcr.io/comfyanonymous/comfyui:latest

WORKDIR /app

# FastAPI
RUN pip install fastapi uvicorn[standard] python-multipart pillow httpx

COPY main.py workflow_img2img.json .
RUN mkdir -p models/controlnet && \
    wget -O models/controlnet/control_v11p_sd15_openpose.pth \
    https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
