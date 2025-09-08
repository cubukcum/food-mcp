# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Sistem bağımlılıkları (CA sertifikaları vs.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Proje dosyaları: pyproject önce (cache için), sonra kaynaklar
COPY pyproject.toml ./
# (Varsa) kilit dosyanızı da kopyalayın ki layer cache iyi çalışsın:
# COPY poetry.lock ./      # Poetry kullanıyorsanız
# COPY pdm.lock ./         # PDM kullanıyorsanız

# Kaynak kod
COPY . .

# Bağımlılıklar + paket kurulumu (PEP 517 üzerinden)
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir .

# Non-root kullanıcı
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Varsayılan ortam değişkenleri
ENV MCP_HOST=0.0.0.0 \
    MCP_PORT=8001

EXPOSE 8001

# Uygulamayı başlat
CMD ["python", "-u", "main.py"]