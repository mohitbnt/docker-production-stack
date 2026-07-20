FROM python:3.12-slim

# =============================================================================
# Build Arguments
# =============================================================================

ARG PROJECT_NAME
ARG BACKEND_IMAGE_VERSION

# =============================================================================
# Image Metadata
# =============================================================================

LABEL org.opencontainers.image.title="${PROJECT_NAME} Backend" \
      org.opencontainers.image.description="Flask backend for ${PROJECT_NAME}" \
      org.opencontainers.image.version="${BACKEND_IMAGE_VERSION}" \
      org.opencontainers.image.authors="Mohit Kumar"

# =============================================================================
# Environment
# =============================================================================

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =============================================================================
# Create Application User
# =============================================================================

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# =============================================================================
# Install System Dependencies
# =============================================================================

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# =============================================================================
# Install Python Dependencies
# =============================================================================

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Copy Application
# =============================================================================

COPY app ./app
COPY gunicorn_conf.py .
COPY wsgi.py .
COPY entrypoint.sh .

# =============================================================================
# Permissions
# =============================================================================

RUN chmod +x /app/entrypoint.sh && \
    chown -R appuser:appuser /app

USER appuser

# =============================================================================
# Network
# =============================================================================

EXPOSE 8000

# =============================================================================
# Health Check
# =============================================================================

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD curl -fsS http://127.0.0.1:8000/api/health || exit 1

# =============================================================================
# Container Startup
# =============================================================================

ENTRYPOINT ["/app/entrypoint.sh"]