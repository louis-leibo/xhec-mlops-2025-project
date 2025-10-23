# MLOps Project: Abalone Age Prediction

[![Python Version](https://img.shields.io/badge/python-3.10%20or%203.11-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](https://github.com/artefactory/xhec-mlops-project-student/blob/main/.pre-commit-config.yaml)

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

## �📚 Project Structure

This project follows a branch-based workflow. Each numbered branch (`0/environment_setup`, `1/eda_and_modelling_notebooks`, etc.) represents a development milestone.

---

## 👥 Contributors

- **Thibaud**
