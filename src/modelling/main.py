"""Main training flow for the abalone age prediction model."""

# isort: off
import sys
from pathlib import Path

# Add src directory to Python path BEFORE other imports
sys.path.insert(0, str(Path(__file__).parent.parent))
# isort: on

import argparse

import mlflow
import mlflow.sklearn
from prefect import flow

from modelling.preprocessing import (
    create_preprocessor,
    load_data,
    prepare_features,
    split_data,
)
from modelling.training import evaluate_model, train_model
from modelling.utils import pickle_object


@flow(name="model_training_flow", version="1.0")
def training_pipeline(trainset_path: str) -> None:
    """
    Train a model using the data at the given path and save the model (pickle).
    Tracks experiments and models with MLflow.

    Args:
        trainset_path: Path to the training dataset CSV file
    """
    # Set MLflow tracking URI and experiment
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("abalone-age-prediction")

    print("=" * 50)
    print("Starting model training pipeline")
    print("=" * 50)

    # Start MLflow run
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("trainset_path", trainset_path)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("model_type", "LinearRegression")

        # Read data
        print(f"\n1. Loading data from {trainset_path}...")
        df = load_data(trainset_path)
        print(f"   Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

        # Log dataset info
        mlflow.log_param("n_samples", df.shape[0])
        mlflow.log_param("n_features", df.shape[1])

        # Preprocess data
        print("\n2. Preparing features and target...")
        X, y = prepare_features(df)

        print("\n3. Splitting data into train/test sets...")
        X_train, X_test, y_train, y_test = split_data(
            X, y, test_size=0.2, random_state=42
        )
        print(f"   Train shape: {X_train.shape}")
        print(f"   Test shape: {X_test.shape}")

        print("\n4. Creating preprocessor...")
        preprocessor = create_preprocessor()

        # Train model
        print("\n5. Training model...")
        model = train_model(preprocessor, X_train, y_train)
        print("   Model training completed!")

        # Evaluate model
        print("\n6. Evaluating model on test set...")
        metrics = evaluate_model(model, X_test, y_test)
        print(f"   MAE  : {metrics['mae']:.3f}")
        print(f"   RMSE : {metrics['rmse']:.3f}")
        print(f"   R²   : {metrics['r2']:.3f}")

        # Log metrics to MLflow
        mlflow.log_metric("mae", metrics["mae"])
        mlflow.log_metric("rmse", metrics["rmse"])
        mlflow.log_metric("r2", metrics["r2"])

        # Pickle model
        print("\n7. Saving model...")
        model_path = (
            Path(__file__).parent.parent / "web_service" / "local_objects" / "model.pkl"
        )
        pickle_object(model, model_path)

        # Log model to MLflow with auto-logging
        print("\n8. Logging model to MLflow...")
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="abalone-age-predictor",
            signature=mlflow.models.infer_signature(X_train, model.predict(X_train)),
        )

        # Log model artifact
        mlflow.log_artifact(str(model_path), "model_artifacts")

        print(f"   MLflow Run ID: {mlflow.active_run().info.run_id}")

        print("\n" + "=" * 50)
        print("Training pipeline completed successfully!")
        print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument("trainset_path", type=str, help="Path to the training set")
    args = parser.parse_args()
    training_pipeline(args.trainset_path)
