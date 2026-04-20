# pipeline_api/Dockerfile
# Source baked in to bypass snap docker bind-mount limitations.
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn "httpx<1"
COPY gateway.py .
CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8000"]
