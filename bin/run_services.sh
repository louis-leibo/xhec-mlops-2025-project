#!/bin/bash
# Script to run the Abalone Age Prediction API services
# Usage: ./bin/run_services.sh [local|docker]

set -e  # Exit on error

echo "============================================"
echo "  Abalone Age Prediction API Services"
echo "============================================"
echo ""

# Check if argument is provided
MODE=${1:-local}

if [ "$MODE" = "docker" ]; then
    echo "🐳 Starting services in Docker mode..."
    echo ""
    
    # Build the Docker image
    echo "Building Docker image..."
    if ! docker build -f Dockerfile.app -t abalone-api:latest .; then
        echo "❌ Docker build failed!"
        echo "💡 Try using the alternative pip-based Dockerfile:"
        echo "   docker build -f Dockerfile.app.pip -t abalone-api:latest ."
        exit 1
    fi
    
    echo ""
    echo "Starting container with port mapping:"
    echo "  - API: http://localhost:8000 (mapped from container port 8001)"
    echo "  - Prefect UI: http://localhost:4200 (mapped from container port 4201)"
    echo ""
    
    # Run the container with port mapping as specified in PR_4.md
    docker run -d \
        --name abalone-api \
        -p 0.0.0.0:8000:8001 \
        -p 0.0.0.0:4200:4201 \
        abalone-api:latest
    
    echo "✅ Container started successfully!"
    echo ""
    echo "📋 Useful commands:"
    echo "  - View logs: docker logs -f abalone-api"
    echo "  - Stop container: docker stop abalone-api"
    echo "  - Remove container: docker rm abalone-api"
    echo ""
    echo "🌐 Access points:"
    echo "  - API Documentation: http://localhost:8000/docs"
    echo "  - Health Check: http://localhost:8000/health"
    echo "  - Prefect UI: http://localhost:4200"
    
elif [ "$MODE" = "local" ]; then
    echo "🏠 Starting services in local mode..."
    echo ""
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo "ERROR: Virtual environment not found!"
        echo "Please run: uv sync --all-extras"
        exit 1
    fi
    
    # Activate virtual environment if not already activated
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    fi
    
    echo "🚀 Starting FastAPI server on port 8001..."
    echo "   API Documentation: http://localhost:8001/docs"
    echo "   Health Check: http://localhost:8001/health"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Start FastAPI server
    uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 --reload
    
else
    echo "❌ Invalid mode: $MODE"
    echo ""
    echo "Usage: $0 [local|docker]"
    echo ""
    echo "Modes:"
    echo "  local  - Run API locally with uvicorn (default)"
    echo "  docker - Build and run API in Docker container"
    echo ""
    exit 1
fi