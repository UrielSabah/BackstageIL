# BackstageIL API - Docker image (Render-compatible)
# Render sets PORT at runtime; default 10000 for local/docker-compose.

FROM python:3.13-slim AS builder

WORKDIR /build

# Install dependencies in a virtual env for a smaller final image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.13-slim AS runtime

WORKDIR /app

# Use the venv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Non-root user (Render and security best practice)
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

# Application code (static/ is needed for ads.txt)
COPY --chown=appuser:appuser . .

# So that uvicorn can resolve app.main from any CWD
ENV PYTHONPATH=/app
# Render sets PORT; default for local/docker-compose
ENV PORT=10000
EXPOSE 10000

# Bind to 0.0.0.0 so Render can reach the app; use PORT at runtime
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
