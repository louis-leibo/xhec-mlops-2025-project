"""Pydantic models for the web service."""

from typing import Literal

from pydantic import BaseModel, Field


class AbaloneFeatures(BaseModel):
    """Features for abalone age prediction."""

    sex: Literal["M", "F", "I"] = Field(
        ..., description="Sex of the abalone: M (Male), F (Female), I (Infant)"
    )
    length: float = Field(..., ge=0.0, le=1.0, description="Length of the abalone (mm)")
    diameter: float = Field(
        ..., ge=0.0, le=1.0, description="Diameter of the abalone (mm)"
    )
    height: float = Field(..., ge=0.0, le=1.0, description="Height of the abalone (mm)")
    whole_weight: float = Field(
        ..., ge=0.0, description="Whole weight of the abalone (grams)"
    )
    shucked_weight: float = Field(
        ..., ge=0.0, description="Shucked weight of the abalone (grams)"
    )
    viscera_weight: float = Field(
        ..., ge=0.0, description="Viscera weight of the abalone (grams)"
    )
    shell_weight: float = Field(
        ..., ge=0.0, description="Shell weight of the abalone (grams)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "sex": "M",
                "length": 0.455,
                "diameter": 0.365,
                "height": 0.095,
                "whole_weight": 0.514,
                "shucked_weight": 0.2245,
                "viscera_weight": 0.101,
                "shell_weight": 0.15,
            }
        }


class PredictionResponse(BaseModel):
    """Response model for abalone age prediction."""

    predicted_rings: float = Field(
        ..., description="Predicted number of rings (age indicator)"
    )
    predicted_age: float = Field(
        ..., description="Predicted age in years (rings + 1.5)"
    )

    class Config:
        json_schema_extra = {"example": {"predicted_rings": 8.5, "predicted_age": 10.0}}


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")

    class Config:
        json_schema_extra = {
            "example": {"status": "healthy", "message": "API is running successfully"}
        }
