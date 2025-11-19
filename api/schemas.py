from pydantic import BaseModel, Field
from typing import Dict, Optional, Any


class SoilInput(BaseModel):
    N: float = Field(..., ge=0, description="Available Nitrogen (kg/ha)")
    P: float = Field(..., ge=0, description="Available Phosphorus (kg/ha)")
    K: float = Field(..., ge=0, description="Available Potassium (kg/ha)")
    pH: Optional[float] = Field(None, ge=0, le=14)
    EC: Optional[float] = Field(None, ge=0)
    Zn: Optional[float] = Field(None, ge=0)
    Fe: Optional[float] = Field(None, ge=0)


class RecommendationRequest(BaseModel):
    soil: SoilInput
    crop: str
    condition: Optional[str] = "Irrigated"
    target_yield: Optional[float] = None
    organic_inputs: Optional[Dict[str, float]] = None
    meta: Optional[Dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    status: str
    method_used: str
    alerts: list
    soil_status: dict
    breakdown: dict
    commercial_fertilizer: dict
