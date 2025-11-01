"""
Prediction API Routes
Main endpoint for market predictions based on planetary transits
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, AsyncGenerator
from datetime import datetime, date
import json

from app.database.config import get_db
from app.schemas.schemas import PredictRequest, PredictResponse
from app.services.prediction_service import PredictionService
from app.services.prediction_cache_service import PredictionCacheService

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
    
    CACHING: Results are cached by date. If a prediction for today already exists,
    it will be returned from cache without calling the AI or market data APIs.
    
    Args:
        request: Prediction parameters (all optional)
        analyse_past: Include historical market data analysis
        stream: Stream the LLM response (future enhancement)
        db: Database session
        
    Returns:
        PredictResponse with planetary transits and market prediction
    """
    try:
        # Get prediction date (default to today)
        prediction_date = date.fromisoformat(request.date) if request.date else date.today()
        
        # Check cache first
        cache_service = PredictionCacheService(db)
        cached_result = cache_service.get_prediction_cache(prediction_date)
        
        if cached_result:
            print(f"✅ Returning cached prediction for {prediction_date}")
            db.commit()
            return cached_result
        
        # No cache hit - generate new prediction
        print(f"❌ Cache miss for {prediction_date} - generating new prediction")
        
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
        
        # Save to cache (convert Pydantic model to dict)
        response_dict = prediction_result.model_dump() if hasattr(prediction_result, 'model_dump') else prediction_result.dict()
        cache_service.save_prediction_cache(prediction_date, response_dict)
        db.commit()
        
        print(f"✅ Saved prediction to cache for {prediction_date}")
        
        return prediction_result
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for prediction service"""
    return {
        "status": "healthy",
        "service": "AstroFinanceAI Prediction Service",
        "timestamp": datetime.utcnow().isoformat()
    }


async def stream_prediction_generator(
    request: PredictRequest,
    analyse_past: bool = False
) -> AsyncGenerator[str, None]:
    """
    Generator function that yields SSE-formatted chunks of prediction data
    """
    try:
        # Initialize services
        prediction_service = PredictionService()
        
        # Yield start status
        yield f"data: {json.dumps({'status': 'started', 'message': 'Generating prediction...'})}\n\n"
        
        # Parse inputs
        prediction_date = date.fromisoformat(request.date) if request.date else date.today()
        yield f"data: {json.dumps({'status': 'processing', 'stage': 'calculating_transits', 'date': str(prediction_date)})}\n\n"
        
        # Generate prediction in chunks (simulate streaming)
        prediction_result = prediction_service.generate_prediction(
            request=request,
            include_past_data=analyse_past
        )
        
        # Convert to dict for streaming
        result_dict = prediction_result.model_dump() if hasattr(prediction_result, 'model_dump') else prediction_result.dict()
        
        # Yield planetary transits first
        yield f"data: {json.dumps({'status': 'processing', 'stage': 'transits', 'data': result_dict.get('planetary_transits', [])})}\n\n"
        
        # Yield market prediction
        if 'market_prediction' in result_dict:
            yield f"data: {json.dumps({'status': 'processing', 'stage': 'market_prediction', 'data': result_dict['market_prediction']})}\n\n"
        
        # Yield confidence
        yield f"data: {json.dumps({'status': 'processing', 'stage': 'confidence', 'data': result_dict.get('confidence', 0)})}\n\n"
        
        # Yield complete status
        yield f"data: {json.dumps({'status': 'complete', 'message': 'Prediction generated successfully'})}\n\n"
        
    except Exception as e:
        # Yield error
        yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"


@router.post("/stream")
async def predict_market_stream(
    request: PredictRequest,
    analyse_past: bool = Query(False, description="Whether to include historical market data analysis"),
    db: Session = Depends(get_db)
):
    """
    Stream market prediction based on planetary transits using Server-Sent Events (SSE)
    
    This endpoint streams prediction results in real-time as they're generated.
    Useful for providing live feedback to users during long-running predictions.
    """
    return StreamingResponse(
        stream_prediction_generator(request, analyse_past),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


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
