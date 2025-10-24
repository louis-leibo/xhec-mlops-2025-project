"""FastAPI application for abalone age prediction."""

# isort: off
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
# isort: on

import logging

import pandas as pd
from fastapi import FastAPI, HTTPException

from modelling.predicting import load_model
from modelling.predicting import predict as make_prediction
from web_service.lib.models import AbaloneFeatures, HealthResponse, PredictionResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define model path
MODEL_PATH = Path(__file__).parent / "local_objects" / "model.pkl"

# Create FastAPI app
app = FastAPI(
    title="Abalone Age Prediction API",
    description="API for predicting abalone age based on physical measurements",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Service status information
    """
    return HealthResponse(
        status="healthy", message="Abalone Age Prediction API is running successfully"
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """
    Alternative health check endpoint.

    Returns:
        HealthResponse: Service status information
    """
    return health_check()


@app.post("/predict", response_model=PredictionResponse, status_code=200)
def predict_endpoint(payload: AbaloneFeatures) -> PredictionResponse:
    """
    Make a prediction for abalone age based on physical measurements.

    Args:
        payload: AbaloneFeatures containing the physical measurements

    Returns:
        PredictionResponse: Predicted rings and age

    Raises:
        HTTPException: If prediction fails
    """
    try:
        logger.info(f"Making prediction for features: {payload.dict()}")

        # Load model for prediction
        logger.info("Loading model...")
        model = load_model(MODEL_PATH)

        # Convert Pydantic model to DataFrame
        features_dict = payload.dict()
        df = pd.DataFrame([features_dict])

        # Transform column names to match what the model expects
        # The model was trained with capitalized column names and spaces instead of underscores
        column_mapping = {
            "sex": "Sex",
            "length": "Length",
            "diameter": "Diameter",
            "height": "Height",
            "whole_weight": "Whole weight",
            "shucked_weight": "Shucked weight",
            "viscera_weight": "Viscera weight",
            "shell_weight": "Shell weight",
        }
        df = df.rename(columns=column_mapping)

        # Make prediction
        prediction = make_prediction(model, df)
        predicted_rings = float(prediction[0])
        predicted_age = predicted_rings + 1.5  # Age = Rings + 1.5

        result = {"predicted_rings": predicted_rings, "predicted_age": predicted_age}

        logger.info(f"Prediction successful: {result}")
        return PredictionResponse(**result)

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}"
        ) from e
