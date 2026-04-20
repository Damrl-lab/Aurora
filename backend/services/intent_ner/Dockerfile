FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# spacy CLI download builds a malformed URL on this version (3.7.4) -> 404.
# Workaround: install the model wheel directly from the upstream release tarball.
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz
COPY src/ ./src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
