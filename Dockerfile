FROM python:3.12-slim

# ComfyUI + Models (Lightweight)
RUN apt-get update && apt-get install -y wget git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/comfyanonymous/ComfyUI.git .
RUN pip install -r requirements.txt && pip install fastapi uvicorn[standard] pillow python-multipart

# Essential Models
RUN mkdir -p models/checkpoints models/vae models/controlnet && \
    wget -O models/checkpoints/sd15.safetensors "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" && \
    wget -O models/vae/sd15_vae.safetensors "https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors" && \
    wget -O models/controlnet/control_v11p_sd15_openpose.pth "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth"

COPY main.py .
EXPOSE 8188  # ComfyUI port
CMD ["python", "main.py"]
