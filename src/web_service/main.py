"""FastAPI application for abalone age prediction."""

import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .lib.inference import model_inference
from .lib.models import (
    AbaloneFeatures,
    PredictionResponse,
    HealthResponse,
    ModelInfoResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Abalone Age Prediction API",
    description="API for predicting abalone age based on physical measurements",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service status information
    """
    return HealthResponse(
        status="healthy",
        message="Abalone Age Prediction API is running successfully"
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """
    Alternative health check endpoint.
    
    Returns:
        HealthResponse: Service status information
    """
    return health_check()


@app.get("/model/info", response_model=ModelInfoResponse)
def get_model_info() -> ModelInfoResponse:
    """
    Get information about the loaded model.
    
    Returns:
        ModelInfoResponse: Model information including features and type
    """
    try:
        info = model_inference.get_model_info()
        return ModelInfoResponse(**info)
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")


@app.post("/predict", response_model=PredictionResponse, status_code=200)
def predict(payload: AbaloneFeatures) -> PredictionResponse:
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
        
        # Convert Pydantic model to dict
        features = payload.dict()
        
        # Make prediction
        result = model_inference.predict(features)
        
        logger.info(f"Prediction successful: {result}")
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/predict/batch", response_model=Dict[str, Any])
def predict_batch_info() -> Dict[str, Any]:
    """
    Get information about batch prediction capabilities.
    
    Returns:
        Dict: Information about batch prediction
    """
    return {
        "message": "Batch prediction not implemented yet",
        "supported": False,
        "note": "Use the /predict endpoint for single predictions"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Abalone Age Prediction API...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Using port 8001 as specified in PR_4.md
        reload=True,
        log_level="info"
    )
