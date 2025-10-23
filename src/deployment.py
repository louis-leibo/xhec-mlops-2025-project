"""
Prefect deployment script for regular model retraining.

This script creates and serves a deployment that will retrain the model
on a regular schedule.
"""

import sys
from pathlib import Path

from prefect import serve

from modelling.main import training_pipeline

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent
TRAINSET_PATH = PROJECT_ROOT / "data" / "abalone.csv"

if __name__ == "__main__":
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Looking for dataset at: {TRAINSET_PATH}")

    # Verify file exists
    if not TRAINSET_PATH.exists():
        raise FileNotFoundError(f"Training dataset not found at {TRAINSET_PATH}")

    # Create a deployment with a schedule and working directory
    deployment = training_pipeline.to_deployment(
        name="abalone-model-retraining",
        # cron="0 15 25 * *",  # Run daily at 2 AM
        interval=60,  # Daily (in seconds)
        parameters={"trainset_path": str(TRAINSET_PATH)},
    )

    # Run the pipeline once immediately
    training_pipeline(trainset_path=str(TRAINSET_PATH))

    # Serve the deployment (this will keep running)
    print("Starting Prefect deployment server...")
    print("Deployment: abalone-model-retraining")
    print("Schedule: Daily at 2 AM")
    print("\nPress Ctrl+C to stop the server")

    serve(deployment)
