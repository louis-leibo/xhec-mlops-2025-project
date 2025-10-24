#!/bin/bash
# Bash script to start all services with Docker Compose
# Usage: ./start_docker.sh

set -e

echo "============================================"
echo "  Starting Abalone MLOps Platform"
echo "============================================"
echo ""

# Check if Docker is running
echo "Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi
echo "Docker is running!"

# Check if docker-compose is available
echo "Checking docker-compose..."
if command -v docker-compose &> /dev/null; then
    echo "docker-compose found!"
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    echo "docker compose (plugin) found!"
    COMPOSE_CMD="docker compose"
else
    echo "ERROR: docker-compose not found!"
    exit 1
fi

echo ""
echo "Building and starting services..."
echo ""

# Build and start all services
$COMPOSE_CMD up --build -d

echo ""
echo "============================================"
echo "  Services Started Successfully!"
echo "============================================"
echo ""
echo "Access the services at:"
echo "  API:           http://localhost:8001"
echo "  API Docs:      http://localhost:8001/docs"
echo "  Prefect UI:    http://localhost:4200"
echo "  MLflow UI:     http://localhost:5000"
echo ""
echo "Useful commands:"
echo "  View logs:     $COMPOSE_CMD logs -f"
echo "  Stop all:      $COMPOSE_CMD down"
echo "  Restart:       $COMPOSE_CMD restart"
echo "  View status:   $COMPOSE_CMD ps"
echo ""
