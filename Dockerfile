# Dockerfile
FROM --platform=linux/amd64 python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential poppler-utils libglib2.0-0 libxrender1 libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ Pre-download models
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1').save('/app/local_model')"

RUN python -c "from transformers import T5Tokenizer, T5ForConditionalGeneration; \
    T5Tokenizer.from_pretrained('t5-small').save_pretrained('/app/t5_model'); \
    T5ForConditionalGeneration.from_pretrained('t5-small').save_pretrained('/app/t5_model')"

# ✅ Set environment variable for offline loading
ENV MODEL_PATH=/app/local_model
ENV T5_PATH=/app/t5_model

CMD ["python", "extractor1b.py"]
