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

## 🚀 Environment Setup

### Prerequisites
- Python 3.10 or 3.11
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/xhec-mlops-2025-project.git
cd xhec-mlops-2025-project

# Install dependencies
uv sync --all-extras

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Install pre-commit hooks
uv run pre-commit install
```

### Download Dataset

1. Download `abalone.csv` from [Kaggle](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset)
2. Place it in the project root directory

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

## � Model Training with Prefect

This project uses Prefect for orchestrating the model training pipeline with scheduling and monitoring capabilities.

### Quick Start - Automated Setup

The easiest way to start the Prefect server and deployment:

**Windows (PowerShell):**
```powershell
.\start_training.ps1
```

**Linux/Mac:**
```bash
chmod +x start_training.sh
./start_training.sh
```

This script will:
- ✅ Check all dependencies (Prefect, SQLite, etc.)
- ✅ Start the Prefect server in a separate window
- ✅ Run the training pipeline immediately
- ✅ Set up automatic retraining on a schedule

### Manual Setup

If you prefer to run components separately:

#### 1. Start Prefect Server

```bash
# Start the Prefect server (keep this terminal open)
uv run prefect server start --host localhost
```

The Prefect UI will be available at: **http://127.0.0.1:4200**

#### 2. Run Training Pipeline

In a new terminal:

```bash
# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Run the deployment with scheduled retraining
uv run python src/deployment.py
```

### View Flow Runs

Open your browser and navigate to the Prefect UI:
- **URL**: http://127.0.0.1:4200
- View flow runs, logs, and execution history
- Monitor scheduled deployments
- Track model training metrics

### Deployment Configuration

The deployment is configured in `src/deployment.py`:
- **Schedule**: Daily retraining (configurable)
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

## � Model Tracking with MLflow

This project uses MLflow to track experiments, log metrics, and version models.

### View MLflow UI

After running a training pipeline, view the MLflow tracking UI:

```bash
uv run mlflow ui
```

Then open your browser to: **http://127.0.0.1:5000**

### What Gets Tracked

MLflow automatically logs:
- **Parameters**: Dataset path, test size, random state, model type
- **Metrics**: MAE, RMSE, R² score
- **Model**: Versioned model artifacts with signature
- **Artifacts**: Model pickle file

### MLflow Features

- 📈 **Experiment Tracking**: Compare different model runs
- 🏷️ **Model Registry**: Version control for trained models
- 📝 **Run Metadata**: Complete reproducibility information
- 🔍 **Model Comparison**: Side-by-side metric comparisons

### Access Models Programmatically

```python
import mlflow

# Load the latest model version
model = mlflow.sklearn.load_model("models:/abalone-age-predictor/latest")

# Or load a specific run
model = mlflow.sklearn.load_model("runs:/<run_id>/model")
```

### MLflow Data Location

- **Tracking Data**: Stored in `./mlruns` directory
- **Registered Models**: Managed by MLflow Model Registry
- **Note**: The `mlruns` directory is gitignored to avoid tracking large binary files

---

## �📚 Project Structure

This project follows a branch-based workflow. Each numbered branch (`0/environment_setup`, `1/eda_and_modelling_notebooks`, etc.) represents a development milestone.


## 🐳 Docker API Deployment (Step 4)

This section covers deploying the FastAPI service using Docker for production-ready predictions.

### Prerequisites

- Docker installed and running
- Model file available at `src/web_service/local_objects/model.pkl`

### Quick Start - Docker API

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
   curl -X POST "http://localhost:8000/predict" \
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

### Docker Management Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs abalone-api

# Follow logs in real-time
docker logs -f abalone-api

# Stop the container
docker stop abalone-api

# Remove the container
docker rm abalone-api

# Remove the image
docker rmi abalone-api:latest
```

### Troubleshooting

#### Container won't start
```bash
# Check logs for errors
docker logs abalone-api

# Verify model file exists
docker exec abalone-api ls -la /app/src/web_service/local_objects/
```

#### Port already in use
```bash
# Check what's using port 8000
lsof -i :8000

# Use a different port
docker run -d --name abalone-api -p 8001:8001 abalone-api:latest
```

#### Model file missing
```bash
# Ensure model exists before building
ls -la src/web_service/local_objects/model.pkl

# If missing, train the model first
uv run python src/modelling/main.py
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Alternative health check |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation |
| `/model/info` | GET | Model information and metadata |
| `/predict` | POST | Make age predictions |

### Making Predictions

#### Using curl

```bash
curl -X POST "http://localhost:8000/predict" \
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

#### Response Format

```json
{
  "predicted_rings": 9.204333139804156,
  "predicted_age": 10.704333139804156
}
```

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

### Docker Configuration

The Docker setup uses the following port mapping:
- **API**: `localhost:8000` → `container:8001`
- **Prefect UI**: `localhost:4200` → `container:4201`

#### Docker Commands

```bash
# Build the image
docker build -f Dockerfile.app -t abalone-api:latest .

# Run the container
docker run -d --name abalone-api -p 8000:8001 abalone-api:latest

# View logs
docker logs abalone-api

# Stop the container
docker stop abalone-api

# Remove the container
docker rm abalone-api
```

### API Documentation

Once the API is running, you can access:
- **Swagger UI**: http://localhost:8000/docs (or 8001 for local)
- **ReDoc**: http://localhost:8000/redoc (or 8001 for local)

These interfaces allow you to:
- Test the API endpoints interactively
- View request/response schemas
- Download OpenAPI specification

---

## 🚀 Complete Workflow

### 1. Environment Setup
```bash
uv sync --all-extras
source .venv/bin/activate
```

### 2. Model Training (Prefect)
```bash
./start_training.sh
# Access Prefect UI at http://localhost:4200
```

### 3. Docker API Deployment (Step 4)
```bash
# Build and run Docker container
docker build -f Dockerfile.app -t abalone-api:latest .
docker run -d --name abalone-api -p 8000:8001 abalone-api:latest

# Verify API is running
curl http://localhost:8000/health
```

### 4. Make Predictions
```bash
# Test the API
curl http://localhost:8000/health

# Make predictions via Docker API
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sex": "M", "length": 0.455, "diameter": 0.365, "height": 0.095, "whole_weight": 0.514, "shucked_weight": 0.2245, "viscera_weight": 0.101, "shell_weight": 0.15}'

# Access interactive documentation
# Open browser: http://localhost:8000/docs
```
