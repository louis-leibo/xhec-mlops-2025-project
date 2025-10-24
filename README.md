# MLOps Project: Abalone Age Prediction

[![CI](https://github.com/louis-leibo/xhec-mlops-2025-project/actions/workflows/ci.yaml/badge.svg)](https://github.com/louis-leibo/xhec-mlops-2025-project/actions/workflows/ci.yaml)
[![Python Version](https://img.shields.io/badge/python-3.10%20or%203.11-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory/xhec-mlops-project-student/blob/main/.pre-commit-config.yaml)
![Docker](https://img.shields.io/badge/docker-ready-blue)

## 📋 Overview

MLOps project to predict abalone age using physical measurements instead of counting shell rings under a microscope.

**Dataset**: [Abalone Dataset on Kaggle](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset)

---

## � Prerequisites

Before starting, ensure you have the following installed:

### Required Software
- **Python 3.10 or 3.11**: [Download Python](https://www.python.org/downloads/)
- **uv Package Manager**: [Install uv](https://github.com/astral-sh/uv)
  ```bash
  # Windows (PowerShell)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

  # Linux/Mac
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **SQLite**: Required for Prefect server database
  - **Windows**: Usually pre-installed, or install via [SQLite Downloads](https://www.sqlite.org/download.html)
  - **Linux**: `sudo apt-get install sqlite3` (Ubuntu/Debian) or `sudo yum install sqlite` (RHEL/CentOS)
  - **Mac**: Pre-installed

### Optional (for Docker deployment)
- **Docker Desktop**: [Download Docker](https://www.docker.com/products/docker-desktop/)
  - Includes Docker Compose
  - Required for containerized deployment

### Verify Installation

```bash
# Check Python version
python --version  # Should be 3.10.x or 3.11.x

# Check uv
uv --version

# Check SQLite
sqlite3 --version

# Check Docker (if using Docker deployment)
docker --version
docker compose version
```

---

## 🚀 Environment Setup

### Installation

```bash
# Clone the repository
git clone https://github.com/louis-leibo/xhec-mlops-2025-project.git
cd xhec-mlops-2025-project

# Install dependencies
uv sync --all-extras

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install pre-commit hooks
uv run pre-commit install
```

---

## 🔧 Development

### Managing Dependencies

```bash
# Add a new package
uv add <package>==<version>

# Sync environment
uv sync
```

### Code Quality

Pre-commit hooks automatically run on each commit to:
- Format code with `ruff`
- Check YAML, TOML, and JSON files
- Remove trailing whitespace
- Ensure files end with newline

To run manually:
```bash
uv run pre-commit run --all-files
```

### Running Tests

```bash
uv run pytest
```

---

## 🔄 Model Training with Prefect & MLflow

This project uses Prefect for orchestrating the model training pipeline and MLflow for experiment tracking.

### Option 1: Quick Start - Automated Scripts

The easiest way to start training with automated setup:

**Windows (PowerShell):**
```powershell
.\start_training.ps1
```

**Linux/Mac:**
```bash
chmod +x start_training.sh
./start_training.sh
```

These scripts will:
- ✅ Check all dependencies (Prefect, SQLite, etc.)
- ✅ Start the Prefect server in a separate window
- ✅ Run the training pipeline immediately
- ✅ Set up automatic retraining on a schedule

### Option 2: Manual CLI Setup (Detailed Steps)

For full control, run each component manually from the command line.

#### Step 1: Start Prefect Server

Open a **new terminal** (keep it running throughout):

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
uv run prefect server start --host localhost

# Linux/Mac
source .venv/bin/activate
uv run prefect server start --host localhost
```

✅ **Prefect UI**: http://127.0.0.1:4200

#### Step 2: Start MLflow Tracking Server

Open **another new terminal** (keep it running):

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
uv run mlflow ui --host 127.0.0.1 --port 5000

# Linux/Mac
source .venv/bin/activate
uv run mlflow ui --host 127.0.0.1 --port 5000
```

✅ **MLflow UI**: http://127.0.0.1:5000

#### Step 3: Run Training Deployment

Open a **third terminal**:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
uv run python src/deployment.py

# Linux/Mac
source .venv/bin/activate
uv run python src/deployment.py
```

This will:
1. Run the training pipeline immediately
2. Create a deployment for scheduled retraining
3. Start serving the deployment (press Ctrl+C to stop)

#### What Happens During Training

1. **Data Loading**: Loads `data/abalone_trainset.csv`
2. **Preprocessing**: OneHotEncoder for `sex`, StandardScaler for numeric features
3. **Model Training**: LinearRegression pipeline
4. **MLflow Tracking**: Logs parameters, metrics (MAE, RMSE, R²), and model
5. **Model Saving**: Saves to `src/web_service/local_objects/model.pkl`
6. **Model Registry**: Registers model as "abalone-age-predictor" in MLflow

#### View Training Results

- **Prefect UI** (http://127.0.0.1:4200):
  - View flow runs and execution logs
  - Monitor deployment schedules
  - Check task execution times

- **MLflow UI** (http://127.0.0.1:5000):
  - Compare experiment runs
  - View logged metrics and parameters
  - Access model versions and artifacts

#### Deployment Configuration

The deployment is configured in `src/deployment.py`:
- **Schedule**: Daily retraining (86400 seconds)
- **Dataset**: `data/abalone_trainset.csv`
- **Flow**: Defined in `src/modelling/main.py`

To modify the schedule, edit `src/deployment.py`:
```python
deployment = training_pipeline.to_deployment(
    name="abalone-model-retraining",
    interval=86400,  # Daily (in seconds)
    # Or use cron:
    # cron="0 2 * * *",  # Daily at 2 AM
)
```

---

## 🌐 FastAPI Prediction Service (Local CLI)

Run the prediction API locally without Docker using uvicorn.

### Prerequisites

- Virtual environment activated
- Trained model available at `src/web_service/local_objects/model.pkl`
- Run training first if model doesn't exist

### Step-by-Step: Start API Server

#### 1. Ensure Model Exists

```bash
# Check if model file exists
# Windows PowerShell
Test-Path src\web_service\local_objects\model.pkl

# Linux/Mac
ls -la src/web_service/local_objects/model.pkl

# If model doesn't exist, train it first
uv run python src/modelling/main.py
```

#### 2. Start API Server with uvicorn

```bash
# Activate virtual environment
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate

# Start the API server
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 --reload
```

**Command breakdown:**
- `uvicorn`: ASGI server for FastAPI
- `src.web_service.main:app`: Module path to FastAPI app instance
- `--host 0.0.0.0`: Listen on all network interfaces
- `--port 8001`: Run on port 8001
- `--reload`: Auto-reload on code changes (dev mode)

#### 3. Access the API

Once running, access:
- **API Base URL**: http://localhost:8001
- **Interactive Docs (Swagger)**: http://localhost:8001/docs
- **Alternative Docs (ReDoc)**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

#### 4. Test the API

**Using curl (PowerShell/Bash):**
```bash
# Health check
curl http://localhost:8001/health

# Make a prediction
curl -X POST "http://localhost:8001/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

**Using Python:**
```python
import requests

url = "http://localhost:8001/predict"
data = {
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
}

response = requests.post(url, json=data)
print(response.json())
# Output: {"predicted_rings": 9.204, "predicted_age": 10.704}
```

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint (health check) |
| `/health` | GET | Health check endpoint |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation |
| `/predict` | POST | Make age predictions |

#### Input Schema

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `sex` | string | Sex of the abalone | "M", "F", or "I" |
| `length` | float | Length (mm) | 0.0 ≤ value ≤ 1.0 |
| `diameter` | float | Diameter (mm) | 0.0 ≤ value ≤ 1.0 |
| `height` | float | Height (mm) | 0.0 ≤ value ≤ 1.0 |
| `whole_weight` | float | Whole weight (grams) | ≥ 0.0 |
| `shucked_weight` | float | Shucked weight (grams) | ≥ 0.0 |
| `viscera_weight` | float | Viscera weight (grams) | ≥ 0.0 |
| `shell_weight` | float | Shell weight (grams) | ≥ 0.0 |

#### Stop the Server

Press `Ctrl+C` in the terminal to stop the uvicorn server.

---

## � Full Docker Compose Deployment

Deploy all services (API, MLflow, Prefect, Training) using Docker Compose.

### Prerequisites

- Docker Desktop installed and running
- Docker Compose available (included with Docker Desktop)

### Step-by-Step: Docker Compose Deployment

#### 1. Build and Launch All Services

```bash
# Navigate to project directory
cd xhec-mlops-2025-project

# Build and start all services in detached mode
docker compose up --build -d
```

**What this does:**
- Builds Docker images for all services
- Creates Docker network for inter-service communication
- Creates shared volumes for data, models, and MLflow artifacts
- Starts all containers in the background

#### 2. Verify Services are Running

```bash
# Check container status
docker compose ps

# View logs for all services
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View logs for specific service
docker compose logs api
docker compose logs mlflow
docker compose logs prefect
docker compose logs training
```

#### 3. Access Service UIs

Once running:
- **API (FastAPI)**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **MLflow UI**: http://localhost:5000
- **Prefect UI**: http://localhost:4200

#### 4. Test the Deployed API

```bash
# Health check
curl http://localhost:8001/health

# Make a prediction
curl -X POST "http://localhost:8001/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

#### 5. Stop Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v

# Stop without removing containers
docker compose stop

# Restart services
docker compose restart
```

### Docker Compose Services

The `docker-compose.yml` defines 4 services:

| Service | Port | Description |
|---------|------|-------------|
| **api** | 8001 | FastAPI prediction service |
| **mlflow** | 5000 | MLflow tracking server |
| **prefect** | 4200 | Prefect orchestration server |
| **training** | N/A | Training service with scheduled deployments |

### Shared Volumes

- `./src` → `/app/src`: Source code
- `./data` → `/app/data`: Training datasets
- `./mlruns` → `/app/mlruns`: MLflow experiment tracking
- `./models` → `/app/models`: Saved model files

### Docker Compose Management

```bash
# View service logs
docker compose logs -f [service_name]

# Rebuild specific service
docker compose build [service_name]

# Restart specific service
docker compose restart [service_name]

# Execute command in running container
docker compose exec api bash

# View resource usage
docker stats

# Remove all stopped containers and unused images
docker system prune -a
```

### Automated Launch Scripts

For convenience, use the provided scripts:

**Windows (PowerShell):**
```powershell
.\start_docker.ps1
```

**Linux/Mac:**
```bash
chmod +x start_docker.sh
./start_docker.sh
```

---

## �📚 Project Structure

This project follows a branch-based workflow. Each numbered branch (`0/environment_setup`, `1/eda_and_modelling_notebooks`, etc.) represents a development milestone.


## 🐳 Single Container Docker Deployment (Alternative)

Alternatively, you can run just the API service in a single Docker container.

### Prerequisites

- Docker installed and running
- Model file available at `src/web_service/local_objects/model.pkl`

### Quick Start - Single Docker Container

#### 1. Build and Run the Docker Container

```bash
# Build the Docker image
docker build -f Dockerfile.app -t abalone-api:latest .

# Run the container with port mapping
docker run -d --name abalone-api -p 8000:8001 abalone-api:latest
```

#### 2. Verify the API is Running

```bash
# Check container status
docker ps

# View logs
docker logs abalone-api

# Test health endpoint
curl http://localhost:8000/health
```

#### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Complete Docker Workflow

#### Step-by-Step Instructions

1. **Navigate to project directory**:
   ```bash
   cd xhec-mlops-2025-project
   ```

2. **Ensure model file exists**:
   ```bash
   ls -la src/web_service/local_objects/model.pkl
   ```

3. **Build Docker image**:
   ```bash
   docker build -f Dockerfile.app -t abalone-api:latest .
   ```

4. **Stop any existing container**:
   ```bash
   # PowerShell
   docker stop abalone-api; docker rm abalone-api

   # Bash
   docker stop abalone-api 2>/dev/null || true
   docker rm abalone-api 2>/dev/null || true
   ```

5. **Run the container**:
   ```bash
   docker run -d --name abalone-api -p 8000:8001 abalone-api:latest
   ```

6. **Test the API**:
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Make a prediction
   curl -X POST "http://localhost:8000/predict" `
     -H "Content-Type: application/json" `
     -d '{
       "sex": "M",
       "length": 0.455,
       "diameter": 0.365,
       "height": 0.095,
       "whole_weight": 0.514,
       "shucked_weight": 0.2245,
       "viscera_weight": 0.101,
       "shell_weight": 0.15
     }'
   ```

### Single Container Management

```bash
# View running containers
docker ps

# View container logs
docker logs abalone-api
docker logs -f abalone-api  # Follow logs

# Stop the container
docker stop abalone-api

# Remove the container
docker rm abalone-api

# Remove the image
docker rmi abalone-api:latest
```

### Troubleshooting Single Container

```bash
# Check logs for errors
docker logs abalone-api

# Verify model file exists in container
docker exec abalone-api ls -la /app/src/web_service/local_objects/

# Port already in use? Use different port
docker run -d --name abalone-api -p 8002:8001 abalone-api:latest
```

---

## 🚀 Complete Deployment Workflows

### Workflow 1: Local Development (CLI Only)

**Use case:** Development, debugging, and testing locally

```bash
# 1. Setup environment
uv sync --all-extras
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac

# 2. Start Prefect server (Terminal 1)
uv run prefect server start --host localhost

# 3. Start MLflow server (Terminal 2)
uv run mlflow ui --host 127.0.0.1 --port 5000

# 4. Run training deployment (Terminal 3)
uv run python src/deployment.py

# 5. Start API server (Terminal 4)
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 --reload

# Access:
# - API: http://localhost:8001/docs
# - Prefect: http://localhost:4200
# - MLflow: http://localhost:5000
```

### Workflow 2: Automated Local Setup

**Use case:** Quick local setup with scripts

```bash
# Windows
.\start_training.ps1

# Linux/Mac
./start_training.sh

# Then in another terminal, start API:
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 --reload
```

### Workflow 3: Full Docker Compose (Recommended for Production)

**Use case:** Complete deployment with all services

```bash
# Build and start all services
docker compose up --build -d

# Access:
# - API: http://localhost:8001/docs
# - Prefect: http://localhost:4200
# - MLflow: http://localhost:5000

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

### Workflow 4: Single Docker Container (API Only)

**Use case:** Deploy only the prediction API

```bash
# Build and run
docker build -f Dockerfile.app -t abalone-api:latest .
docker run -d --name abalone-api -p 8000:8001 abalone-api:latest

# Access API: http://localhost:8000/docs

# Stop
docker stop abalone-api
docker rm abalone-api
```

---

## 📊 Quick Reference: Deployment Comparison

| Method | Setup Time | Use Case | Services | Ports |
|--------|------------|----------|----------|-------|
| **Local CLI** | Slow | Development | All | 8001, 4200, 5000 |
| **Automated Scripts** | Fast | Development | Prefect + Training | 4200, 5000 |
| **Docker Compose** | Medium | Production | All | 8001, 4200, 5000 |
| **Single Container** | Fast | API Only | API only | 8000 |

---

## 🧪 Testing Your Deployment

### Test API Endpoint

```bash
# Health check
curl http://localhost:8001/health

# Prediction (adjust port based on deployment method)
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

**Expected response:**
```json
{
  "predicted_rings": 9.204333139804156,
  "predicted_age": 10.704333139804156
}
```

### Verify Training Pipeline

1. Access Prefect UI: http://localhost:4200
2. Check "Flow Runs" tab for completed runs
3. Verify "training-pipeline" shows successful execution

### Verify MLflow Tracking

1. Access MLflow UI: http://localhost:5000
2. Check "Experiments" for logged runs
3. Verify metrics (MAE, RMSE, R²) are recorded
4. Check "Models" for registered "abalone-age-predictor"

---

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
# Windows
netstat -ano | findstr :8001

# Linux/Mac
lsof -i :8001

# Kill the process or use different port
```

#### Model File Not Found
```bash
# Train the model first
uv run python src/modelling/main.py

# Verify model exists
ls -la src/web_service/local_objects/model.pkl
```

#### Prefect Server Won't Start
```bash
# Check SQLite is installed
sqlite3 --version

# Reset Prefect database
prefect server database reset -y
```

#### Docker Compose Fails
```bash
# View logs for specific service
docker compose logs training

# Rebuild specific service
docker compose build training
docker compose up training

# Clean restart
docker compose down -v
docker compose up --build -d
```

---

## 📚 Additional Resources

- **Prefect Documentation**: https://docs.prefect.io/
- **MLflow Documentation**: https://mlflow.org/docs/latest/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/

---

## 📝 Project Structure

This project follows a branch-based workflow. Each numbered branch represents a development milestone:
- `0/environment_setup`: Initial setup
- `1/eda_and_modelling_notebooks`: Exploratory analysis
- `2/package_code`: Code organization
- `3/use_prefect`: Workflow orchestration (current)
- `4/containerization`: Docker deployment
