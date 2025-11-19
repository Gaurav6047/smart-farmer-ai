from fastapi import APIRouter, HTTPException
from ..schemas import RecommendationRequest, RecommendationResponse
from ...engine.recommender import FertilizerRecommender

router = APIRouter()

recommender = FertilizerRecommender()  # Singleton-like behaviour


@router.post("/recommend", response_model=RecommendationResponse, tags=["Fertilizer"])
async def recommend_fertilizer(request: RecommendationRequest):

    try:
        result = recommender.recommend(
            soil=request.soil.dict(),
            crop=request.crop,
            condition=request.condition,
            target_yield=request.target_yield,
            organic_inputs=request.organic_inputs or {},
            meta=request.meta or {}
        )

        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Fertilizer Engine Error: {str(e)}"
        )
