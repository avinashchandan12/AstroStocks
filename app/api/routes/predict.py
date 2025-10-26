"""
Prediction API Routes
Main endpoint for market predictions based on planetary transits
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from app.database.config import get_db
from app.schemas.schemas import PredictRequest, PredictResponse
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("", response_model=PredictResponse)
async def predict_market(
    request: PredictRequest,
    analyse_past: bool = Query(False, description="Whether to include historical market data analysis"),
    stream: bool = Query(False, description="Whether to stream the LLM response"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate market prediction based on planetary transits
    
    This endpoint calculates planetary positions for a specific date/time/location
    and generates AI-powered market predictions based on Vedic astrology principles.
    
    Args:
        request: Prediction parameters (all optional)
        analyse_past: Include historical market data analysis
        stream: Stream the LLM response (future enhancement)
        db: Database session
        
    Returns:
        PredictResponse with planetary transits and market prediction
    """
    try:
        # Initialize prediction service
        prediction_service = PredictionService()
        
        # Generate prediction
        prediction_result = prediction_service.generate_prediction(
            request=request,
            include_past_data=analyse_past
        )
        
        # TODO: Implement streaming support in Phase 2
        if stream:
            print("⚠️  Streaming not yet implemented, returning standard response")
        
        return prediction_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for prediction service"""
    return {
        "status": "healthy",
        "service": "AstroFinanceAI Prediction Service",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/test")
async def test_prediction():
    """Test endpoint for prediction service"""
    try:
        # Create test request with default values
        test_request = PredictRequest()
        
        # Initialize prediction service
        prediction_service = PredictionService()
        
        # Generate test prediction
        result = prediction_service.generate_prediction(
            request=test_request,
            include_past_data=False
        )
        
        return {
            "message": "Test prediction successful",
            "prediction_date": result.prediction_date,
            "planetary_transits_count": len(result.planetary_transits),
            "overall_sentiment": result.market_prediction.overall_sentiment,
            "confidence": result.confidence
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test prediction failed: {str(e)}")
