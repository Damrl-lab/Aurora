# services/deepseek_llm/Dockerfile
FROM nvidia/cuda:12.9.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       python3 python3-pip git libnuma-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
      torch==2.5.1+cu124 torchvision==0.20.1+cu124 \
      --extra-index-url https://download.pytorch.org/whl/cu124

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY server.py serve.sh ./

RUN chmod +x serve.sh


ENV MODEL_ID="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B" \
    HF_HOME="/hf_cache"
RUN python3 - <<'PY'
from huggingface_hub import snapshot_download
import os
snapshot_download(
    os.environ["MODEL_ID"],
    local_dir="/app/model",
    cache_dir=os.environ["HF_HOME"],
    local_dir_use_symlinks=False
)
PY


ENTRYPOINT ["./serve.sh"]
CMD []
