# Dockerfile for Abalone Age Prediction API - Minimal version
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy source code first
COPY src/ ./src/
COPY data/ ./data/

# Install only the essential Python packages directly
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pandas \
    scikit-learn \
    numpy \
    pydantic \
    mlflow>=2.8.0 \
    prefect>=3.4.0

# Ensure model directory exists
RUN mkdir -p src/web_service/local_objects

# Expose API port
EXPOSE 8001

# Set environment variables
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Default command to run the API
CMD ["uvicorn", "src.web_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
