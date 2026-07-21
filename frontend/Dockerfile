# =============================================================================
# Stage 1 - React Build
# =============================================================================

FROM node:22-alpine AS builder

ARG PROJECT_NAME
ARG IMAGE_VERSION

LABEL org.opencontainers.image.title="${PROJECT_NAME} Frontend"
LABEL org.opencontainers.image.description="React/Vite build for ${PROJECT_NAME}"
LABEL org.opencontainers.image.version="${IMAGE_VERSION}"
LABEL org.opencontainers.image.authors="Mohit Kumar"

WORKDIR /app

# Copy dependency files first (better layer caching)
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy application source
COPY frontend/ .


# Build production assets
RUN npm run build

# =============================================================================
# Stage 2 - Nginx Runtime
# =============================================================================

FROM nginx:1.28-alpine

ARG PROJECT_NAME

LABEL org.opencontainers.image.title="${PROJECT_NAME} Frontend Runtime"

# Remove default web content
RUN rm -rf /usr/share/nginx/html/*

# Copy React build
COPY --from=builder /app/dist/ /usr/share/nginx/html/

# Copy Nginx configuration
COPY nginx/opsportal.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
CMD wget --quiet --spider http://127.0.0.1/ || exit 1

CMD ["nginx","-g","daemon off;"]