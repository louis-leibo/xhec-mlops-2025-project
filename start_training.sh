#!/bin/bash
# Bash script to start Prefect server and model retraining deployment
# Usage: ./start_training.sh

set -e  # Exit on error

echo "============================================"
echo "  Prefect Model Training Setup"
echo "============================================"
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

# Check if uv is installed
echo "Checking dependencies..."
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv is not installed!"
    echo "Install from: https://github.com/astral-sh/uv"
    exit 1
fi

# Check if Prefect is installed
echo "Checking Prefect installation..."
if uv run python -c "import prefect; print(f'Prefect version: {prefect.__version__}')" 2>/dev/null; then
    :  # Success, do nothing
else
    echo "Prefect not found. Installing dependencies..."
    uv sync --all-extras
    echo "Dependencies installed successfully!"
fi

# Check SQLite availability (Prefect requirement)
echo "Checking SQLite..."
if uv run python -c "import sqlite3; print(f'SQLite {sqlite3.sqlite_version}')" 2>/dev/null; then
    :  # Success, do nothing
else
    echo "WARNING: SQLite check failed, but it's usually built-in with Python"
fi

echo ""

echo "Starting Prefect server in background..."

# Start Prefect server in background
uv run prefect server start --host localhost > prefect_server.log 2>&1 &
PREFECT_PID=$!

# Wait for server to start
echo "Waiting for Prefect server to initialize (15 seconds)..."
sleep 15

echo ""
echo "============================================"
echo "  Prefect UI available at:"
echo "  http://127.0.0.1:4200"
echo "============================================"
echo ""
echo "Prefect server PID: $PREFECT_PID"
echo "Server logs: prefect_server.log"
echo ""

echo "Starting model retraining deployment..."
echo ""

# Run the deployment script
uv run python src/web_service/model_training.py

# Clean up: kill Prefect server on exit
trap "kill $PREFECT_PID 2>/dev/null" EXIT
