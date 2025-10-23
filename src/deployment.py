"""
Prefect deployment script for regular model retraining.

This script creates and serves a deployment that will retrain the model
on a regular schedule.
"""

from prefect import serve

from modelling.main import training_pipeline

if __name__ == "__main__":
    # Create a deployment with a schedule
    deployment = training_pipeline.to_deployment(
        name="abalone-model-retraining",
        # cron="0 15 25 * *",  # Run daily at 2 AM
        interval=86400,  # Daily (in seconds)
        parameters={"trainset_path": "data/abalone.csv"},
    )

    training_pipeline(trainset_path="data/abalone.csv")

    # Serve the deployment (this will keep running)
    print("Starting Prefect deployment server...")
    print("Deployment: abalone-model-retraining")
    print("Schedule: Daily at 2 AM")
    print("\nPress Ctrl+C to stop the server")

    serve(deployment)
