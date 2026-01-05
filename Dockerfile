FROM python:3.12-slim

RUN apt-get update && apt-get install -y wget git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/comfyanonymous/ComfyUI.git .
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn[standard] pillow python-multipart torch torchvision

COPY main.py .

EXPOSE 8000
CMD ["sh", "-c", "python ComfyUI/main.py --listen 0.0.0.0 --port 8188 & uvicorn main:app --host 0.0.0.0 --port 8000"]
