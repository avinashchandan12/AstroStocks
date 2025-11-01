"""
Analysis API Routes
Main endpoint for astrological market analysis
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
import os

from app.database.config import get_db
from app.schemas.schemas import AnalyzeRequest, AnalyzeResponse, EnhancedAnalyzeResponse
from app.services.ai_service import AIService
from app.services.ephemeris_service import get_planetary_transits
from app.services.market_data_cache import MarketDataCacheService
from app.config.stock_config import get_tracked_stocks, use_real_market_data
from app.models.models import SectorPrediction

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("", response_model=AnalyzeResponse)
async def analyze_market(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Main analysis endpoint
    
    Combines stock market data with planetary transits to generate
    AI-driven astrological predictions for various sectors.
    
    Requires stock and transit data to be provided in the request.
    """
    try:
        # Require stocks to be provided
        if not request.stocks:
            raise HTTPException(
                status_code=400,
                detail="Stock data is required. Please provide stocks in the request."
            )
        
        stocks = request.stocks
        transits_data = request.transits if request.transits else None
        
        # Convert transits to list format if needed
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
        
        # Initialize AI service
        ai_service = AIService()
        
        # Run analysis
        analysis_result = ai_service.analyze_market(stocks, transits)
        
        # Store predictions in database
        for prediction in analysis_result["sector_predictions"]:
            db_prediction = SectorPrediction(
                sector=prediction["sector"],
                planetary_influence=prediction["planetary_influence"],
                trend=prediction["trend"],
                reason=prediction["reason"],
                top_stocks=prediction["top_stocks"],
                accuracy_estimate=float(analysis_result["accuracy_estimate"].rstrip("%")) / 100
            )
            db.add(db_prediction)
        
        db.commit()
        
        # Return response
        return AnalyzeResponse(
            sector_predictions=analysis_result["sector_predictions"],
            overall_market_sentiment=analysis_result["overall_market_sentiment"],
            accuracy_estimate=analysis_result["accuracy_estimate"],
            timestamp=datetime.fromisoformat(analysis_result["timestamp"])
        )
    
    except HTTPException:
        raise
    except Exception as e:
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
    """
    try:
        # Get stock data (real or from request)
        if use_real_data and use_real_market_data():
            print("📊 Using real market data from Alpha Vantage...")
            cache_service = MarketDataCacheService(db)
            tracked_symbols = get_tracked_stocks()
            
            if not tracked_symbols:
                raise HTTPException(
                    status_code=400,
                    detail="No stocks configured. Set NSE_STOCKS in environment."
                )
            
            stocks = cache_service.get_stock_data(tracked_symbols)
            
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
        
        print(f"✅ Analysis complete: {len(analysis_result['top_recommendations'])} recommendations generated")
        
        # Return enhanced response
        return analysis_result
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AstroFinanceAI Analysis Service",
        "timestamp": datetime.utcnow().isoformat()
    }

