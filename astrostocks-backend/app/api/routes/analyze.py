"""
Analysis API Routes
Main endpoint for astrological market analysis
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, AsyncGenerator
from datetime import datetime, date
import os
import json

from app.database.config import get_db
from app.schemas.schemas import AnalyzeRequest, AnalyzeResponse, EnhancedAnalyzeResponse
from app.services.ai_service import AIService
from app.services.ephemeris_service import get_planetary_transits
from app.services.market_data_cache import MarketDataCacheService
from app.services.prediction_cache_service import PredictionCacheService
from app.config.stock_config import get_tracked_stocks, use_real_market_data
from app.models.models import SectorPrediction, SectorArchive

router = APIRouter(prefix="/analyze", tags=["Analysis"])


def _archive_old_predictions(db: Session, analysis_date: date) -> None:
    """
    Archive old sector predictions to sector_archive table before hard refresh
    
    Args:
        db: Database session
        analysis_date: Date for which predictions are being archived
    """
    from datetime import datetime
    
    # Try to get cached predictions which may have newer fields
    cache_service = PredictionCacheService(db)
    cached_data = cache_service.get_analyze_cache(analysis_date, 'basic')
    
    # Create a mapping of cached predictions by sector name for quick lookup
    cached_predictions_map = {}
    if cached_data and 'sector_predictions' in cached_data:
        for cached_pred in cached_data['sector_predictions']:
            sector_key = cached_pred.get('sector') or cached_pred.get('sector_name', '')
            cached_predictions_map[sector_key] = cached_pred
    
    # Get all existing predictions from database
    old_predictions = db.query(SectorPrediction).all()
    
    if not old_predictions:
        print("⚠️  No old predictions to archive")
        return
    
    archived_count = 0
    for old_pred in old_predictions:
        # Try to get enhanced data from cache
        cached_pred = cached_predictions_map.get(old_pred.sector, {})
        
        # Create archive entry with all available data
        archive_entry = SectorArchive(
            sector=old_pred.sector,
            planetary_influence=old_pred.planetary_influence,
            trend=old_pred.trend,
            reason=old_pred.reason,
            top_stocks=old_pred.top_stocks,
            accuracy_estimate=old_pred.accuracy_estimate,
            sector_id=cached_pred.get('sector_id'),
            sector_name=cached_pred.get('sector_name', old_pred.sector),
            confidence=cached_pred.get('confidence'),
            ai_insights=cached_pred.get('ai_insights'),
            transit_start=cached_pred.get('transit_start'),
            transit_end=cached_pred.get('transit_end'),
            original_created_at=old_pred.created_at,
            archive_date=analysis_date
        )
        db.add(archive_entry)
        archived_count += 1
    
    db.commit()
    print(f"📦 Archived {archived_count} old predictions to sector_archive table for date {analysis_date}")


@router.post("", response_model=AnalyzeResponse)
async def analyze_market(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Main analysis endpoint
    
    Generates AI-driven astrological predictions for all sectors in the database.
    
    Stocks are optional - if not provided, predictions will be generated for all
    sectors with top stocks fetched from the database. If stocks are provided,
    only those sectors will be analyzed.
    
    Transit timing information (start/end dates) is automatically calculated
    and included in the response.
    
    CACHING: Results are cached by date. If an analysis for today already exists,
    it will be returned from cache without calling the AI or market data APIs.
    
    HARD_REFRESH: If hard_refresh=true is passed, cache is bypassed, old predictions
    are archived to sector_archive table, and new analysis is generated.
    """
    try:
        # Get analysis date (default to today)
        analysis_date = date.today()
        hard_refresh = request.hard_refresh if request.hard_refresh else False
        
        cache_service = PredictionCacheService(db)
        
        # Check cache first (unless hard refresh)
        if not hard_refresh:
            cached_result = cache_service.get_analyze_cache(analysis_date, 'basic')
            
            if cached_result:
                print(f"✅ Returning cached analysis for {analysis_date}")
                db.commit()
                return AnalyzeResponse(**cached_result)
        
        # Hard refresh or cache miss - generate new analysis
        if hard_refresh:
            print(f"🔄 Hard refresh requested for {analysis_date} - archiving old predictions and regenerating")
            # Archive old predictions before generating new ones
            _archive_old_predictions(db, analysis_date)
        else:
            print(f"❌ Cache miss for {analysis_date} - generating new analysis")
        
        # Stocks are now optional - if not provided, will predict all sectors from database
        stocks = request.stocks if request.stocks else None
        
        transits_data = request.transits if request.transits else None
        
        # Convert transits to list format if needed
        if transits_data and isinstance(transits_data, dict):
            transits = transits_data.get("transits", [])
        elif transits_data and isinstance(transits_data, list):
            transits = transits_data
        else:
            # Get real transits from ephemeris service (with timing)
            transits = get_planetary_transits()
            
            if not transits:
                raise HTTPException(
                    status_code=503,
                    detail="Planetary transit data unavailable. Please install pyswisseph and configure ephemeris."
                )
        
        # Initialize AI service
        ai_service = AIService()
        
        # Run analysis (stocks optional, will predict all sectors if None)
        analysis_result = ai_service.analyze_market(stocks=stocks, transits=transits, db=db)
        
        # Store predictions in database
        # If hard refresh, delete old predictions first (already archived)
        if hard_refresh:
            old_predictions = db.query(SectorPrediction).all()
            for old_pred in old_predictions:
                db.delete(old_pred)
            db.commit()
            print(f"🗑️  Deleted {len(old_predictions)} old predictions after archiving")
        
        for prediction in analysis_result["sector_predictions"]:
            db_prediction = SectorPrediction(
                sector=prediction.get("sector") or prediction.get("sector_name", ""),
                planetary_influence=prediction.get("planetary_influence"),
                trend=prediction.get("trend"),
                reason=prediction.get("reason"),
                top_stocks=prediction.get("top_stocks"),
                accuracy_estimate=float(analysis_result["accuracy_estimate"].rstrip("%")) / 100 if analysis_result.get("accuracy_estimate") else None
            )
            db.add(db_prediction)
        
        db.commit()
        
        # Return response
        response = AnalyzeResponse(
            sector_predictions=analysis_result["sector_predictions"],
            overall_market_sentiment=analysis_result["overall_market_sentiment"],
            accuracy_estimate=analysis_result["accuracy_estimate"],
            timestamp=datetime.fromisoformat(analysis_result["timestamp"])
        )
        
        # Save to cache (or update if hard refresh)
        if hard_refresh:
            # Delete old cache entry if exists
            old_cache = cache_service.get_analyze_cache(analysis_date, 'basic')
            if old_cache:
                cache_service.delete_analyze_cache(analysis_date, 'basic')
                db.commit()
                print(f"🗑️  Deleted old cache entry for {analysis_date}")
        
        response_dict = response.model_dump() if hasattr(response, 'model_dump') else response.dict()
        cache_service.save_analyze_cache(analysis_date, 'basic', response_dict)
        db.commit()
        
        if hard_refresh:
            print(f"✅ Hard refresh complete: Archived old predictions, generated new analysis, and updated cache for {analysis_date}")
        else:
            print(f"✅ Saved analysis to cache for {analysis_date}")
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/enhanced", response_model=EnhancedAnalyzeResponse)
async def analyze_market_enhanced(
    request: AnalyzeRequest,
    use_real_data: bool = Query(True, description="Use real market data from Alpha Vantage"),
    
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Enhanced analysis endpoint with real market data integration
    
    Returns:
    - Top 5-10 stock recommendations with astrological reasoning
    - Sector-level analysis with all tracked stocks
    - Buy/Hold/Sell signals for each stock
    
    This endpoint combines:
    1. Real NSE stock data from Alpha Vantage (with caching)
    2. Real planetary positions from pyswisseph
    3. DeepSeek AI for astrological insights
    4. Vedic astrology engine for sector analysis
    
    CACHING: Results are cached by date. If an enhanced analysis for today already exists,
    it will be returned from cache without calling the AI or market data APIs.
    """
    try:
        # Get analysis date (default to today)
        analysis_date = date.today()
        
        # Check cache first
        analysis_cache_service = PredictionCacheService(db)
        cached_result = analysis_cache_service.get_analyze_cache(analysis_date, 'enhanced')
        
        if cached_result:
            print(f"✅ Returning cached enhanced analysis for {analysis_date}")
            db.commit()
            return cached_result
        
        # No cache hit - generate new enhanced analysis
        print(f"❌ Cache miss for {analysis_date} - generating new enhanced analysis")
        
        # Get stock data (real or from request)
        if use_real_data and use_real_market_data():
            print("📊 Using real market data from Alpha Vantage...")
            market_cache_service = MarketDataCacheService(db)
            tracked_symbols = get_tracked_stocks()
            
            if not tracked_symbols:
                raise HTTPException(
                    status_code=400,
                    detail="No stocks configured. Set NSE_STOCKS in environment."
                )
            
            stocks = market_cache_service.get_stock_data(tracked_symbols)
            
            if not stocks:
                raise HTTPException(
                    status_code=503,
                    detail="No stock data available from market data service."
                )
        else:
            # Require stocks from request if not using real data
            if not request.stocks:
                raise HTTPException(
                    status_code=400,
                    detail="Stock data is required. Please provide stocks in the request or enable real market data."
                )
            print("📊 Using stock data from request")
            stocks = request.stocks
        
        # Get transit data (real ephemeris)
        transits_data = request.transits if request.transits else None
        if transits_data and isinstance(transits_data, dict):
            transits = transits_data.get("transits", [])
        elif transits_data and isinstance(transits_data, list):
            transits = transits_data
        else:
            # Get real transits from ephemeris service
            transits = get_planetary_transits()
            
            if not transits:
                raise HTTPException(
                    status_code=503,
                    detail="Planetary transit data unavailable. Please install pyswisseph and configure ephemeris."
                )
        
        print(f"🌟 Analyzing {len(stocks)} stocks with {len(transits)} planetary transits...")
        
        # Initialize AI service
        ai_service = AIService()
        
        # Run enhanced analysis
        analysis_result = ai_service.analyze_market_with_stocks(stocks, transits)
        
        # Store sector predictions in database
        for sector_pred in analysis_result["sector_analysis"]:
            # Extract stocks for top_stocks field
            stock_symbols = [s["symbol"] for s in sector_pred.get("stocks_in_sector", [])[:5]]
            
            db_prediction = SectorPrediction(
                sector=sector_pred["sector"],
                planetary_influence=sector_pred["planetary_influence"],
                trend=sector_pred["trend"],
                reason=sector_pred.get("ai_insights", ""),
                top_stocks=stock_symbols,
                accuracy_estimate=sector_pred["confidence"]
            )
            db.add(db_prediction)
        
        db.commit()
        
        # Save to cache
        analysis_cache_service.save_analyze_cache(analysis_date, 'enhanced', analysis_result)
        db.commit()
        
        print(f"✅ Analysis complete: {len(analysis_result['top_recommendations'])} recommendations generated")
        print(f"✅ Saved enhanced analysis to cache for {analysis_date}")
        
        # Return enhanced response
        return analysis_result
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")


async def stream_analysis_generator(
    request: AnalyzeRequest,
    endpoint_type: str = 'basic'
) -> AsyncGenerator[str, None]:
    """
    Generator function that yields SSE-formatted chunks of analysis data
    """
    try:
        # Initialize AI service
        ai_service = AIService()
        
        # Yield start status
        yield f"data: {json.dumps({'status': 'started', 'message': 'Starting analysis...'})}\n\n"
        
        # Get stock data
        if not request.stocks:
            yield f"data: {json.dumps({'status': 'error', 'error': 'Stock data is required'})}\n\n"
            return
        
        stocks = request.stocks
        yield f"data: {json.dumps({'status': 'processing', 'stage': 'loading_data', 'message': f'Analyzing {len(stocks)} stocks...'})}\n\n"
        
        # Get transit data
        transits_data = request.transits if request.transits else None
        if transits_data and isinstance(transits_data, dict):
            transits = transits_data.get("transits", [])
        elif transits_data and isinstance(transits_data, list):
            transits = transits_data
        else:
            transits = get_planetary_transits()
        
        if not transits:
            yield f"data: {json.dumps({'status': 'error', 'error': 'Planetary transit data unavailable'})}\n\n"
            return
        
        yield f"data: {json.dumps({'status': 'processing', 'stage': 'transits_loaded', 'count': len(transits)})}\n\n"
        
        # Run analysis
        if endpoint_type == 'enhanced':
            analysis_result = ai_service.analyze_market_with_stocks(stocks, transits)
        else:
            analysis_result = ai_service.analyze_market(stocks, transits)
        
        # Stream sector predictions
        sector_predictions = analysis_result.get('sector_predictions', [])
        yield f"data: {json.dumps({'status': 'processing', 'stage': 'sectors', 'count': len(sector_predictions)})}\n\n"
        
        # Yield each sector prediction
        for idx, sector_pred in enumerate(sector_predictions):
            yield f"data: {json.dumps({'status': 'processing', 'stage': 'sector_detail', 'index': idx, 'data': sector_pred})}\n\n"
        
        # Yield complete result
        yield f"data: {json.dumps({'status': 'complete', 'data': analysis_result})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"


@router.post("/stream")
async def analyze_market_stream(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Stream market analysis using Server-Sent Events (SSE)
    
    This endpoint streams analysis results in real-time as they're generated.
    """
    return StreamingResponse(
        stream_analysis_generator(request, 'basic'),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/enhanced/stream")
async def analyze_market_enhanced_stream(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Stream enhanced market analysis using Server-Sent Events (SSE)
    
    This endpoint streams enhanced analysis results in real-time.
    """
    return StreamingResponse(
        stream_analysis_generator(request, 'enhanced'),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AstroFinanceAI Analysis Service",
        "timestamp": datetime.utcnow().isoformat()
    }

