# Dockerfile for Abalone Age Prediction API - Minimal version
FROM python:3.11-slim

# Set working directory
WORKDIR /app

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
    pydantic

# Ensure model directory exists
RUN mkdir -p src/web_service/local_objects

# Expose port
EXPOSE 8001

# Set environment variables
ENV PYTHONPATH=/app

# Default command to run the API
CMD ["uvicorn", "src.web_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
