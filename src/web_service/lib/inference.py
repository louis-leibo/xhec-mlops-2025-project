"""Inference module for the FastAPI web service."""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.pipeline import Pipeline

from ...modelling.utils import load_pickle_object

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelInference:
    """Model inference class for making predictions."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the model inference.
        
        Args:
            model_path: Path to the model file. If None, uses default path.
        """
        if model_path is None:
            model_path = (
                Path(__file__).parent.parent.parent / "web_service" / "local_objects" / "model.pkl"
            )
        
        self.model_path = model_path
        self.model: Optional[Pipeline] = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the trained model from pickle file."""
        try:
            logger.info(f"Loading model from {self.model_path}")
            self.model = load_pickle_object(self.model_path)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Could not load model from {self.model_path}")
    
    def predict(self, features: dict) -> dict:
        """
        Make a prediction using the loaded model.
        
        Args:
            features: Dictionary containing abalone features
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        try:
            # Convert features to DataFrame with correct column names
            # Map API field names to model expected names
            feature_mapping = {
                "sex": "Sex",
                "length": "Length", 
                "diameter": "Diameter",
                "height": "Height",
                "whole_weight": "Whole weight",
                "shucked_weight": "Shucked weight", 
                "viscera_weight": "Viscera weight",
                "shell_weight": "Shell weight"
            }
            
            # Create DataFrame with correct column names
            df_data = {feature_mapping[k]: [v] for k, v in features.items()}
            df = pd.DataFrame(df_data)
            
            # Make prediction
            prediction = self.model.predict(df)[0]
            
            # Calculate age (rings + 1.5)
            age = prediction + 1.5
            
            return {
                "predicted_rings": float(prediction),
                "predicted_age": float(age)
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise RuntimeError(f"Prediction failed: {str(e)}")
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        return {
            "model_type": str(type(self.model).__name__),
            "features": [
                "sex", "length", "diameter", "height", 
                "whole_weight", "shucked_weight", "viscera_weight", "shell_weight"
            ],
            "target": "rings",
            "model_path": str(self.model_path)
        }


# Global model instance
model_inference = ModelInference()
