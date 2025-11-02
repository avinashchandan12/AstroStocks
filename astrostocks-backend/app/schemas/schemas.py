from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime


class SectorBase(BaseModel):
    name: str
    description: Optional[str] = None
    past_6m_return: Optional[float] = None
    past_1y_return: Optional[float] = None
    volatility: Optional[str] = None
    market_cap: Optional[float] = None
    exchange: Optional[str] = None
    country: Optional[str] = 'India'


class SectorCreate(SectorBase):
    pass


class Sector(SectorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class StockBase(BaseModel):
    symbol: str
    script_code: Optional[str] = None  # Exchange script code (e.g., NSE, BSE)
    sector: str
    sector_id: Optional[int] = None
    past_6m_return: Optional[float] = None
    volatility: Optional[str] = None
    pe_ratio: Optional[float] = None
    price_trend: Optional[str] = None
    news_sentiment: Optional[str] = None


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    id: int
    
    class Config:
        from_attributes = True


class TransitBase(BaseModel):
    planet: str
    sign: str
    motion: Optional[str] = None
    status: Optional[str] = None
    date: date


class TransitCreate(TransitBase):
    pass


class Transit(TransitBase):
    id: int
    
    class Config:
        from_attributes = True


class SectorPredictionBase(BaseModel):
    sector: str
    planetary_influence: Optional[str] = None
    trend: Optional[str] = None
    reason: Optional[str] = None
    top_stocks: Optional[List[str]] = None
    accuracy_estimate: Optional[float] = None


class SectorPredictionCreate(SectorPredictionBase):
    pass


class SectorPrediction(SectorPredictionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalyzeRequest(BaseModel):
    stocks: Optional[List[Dict[str, Any]]] = Field(
        None, 
        description="Optional list of stock data. If not provided, analysis will be generated for all sectors from database."
    )
    transits: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional planetary transit data. If not provided, real ephemeris data will be fetched."
    )
    hard_refresh: Optional[bool] = Field(
        False,
        description="If true, bypass cache, archive old predictions, and regenerate analysis."
    )


class AnalyzeResponse(BaseModel):
    sector_predictions: List[Dict[str, Any]]
    overall_market_sentiment: str
    accuracy_estimate: str
    timestamp: datetime


class StockSignal(BaseModel):
    """Stock with buy/hold/sell signal and astrological analysis"""
    symbol: str
    sector: str
    current_price: Optional[float] = None
    change_percent: Optional[float] = None
    signal: str  # BUY, HOLD, SELL
    confidence: float
    astrological_reasoning: str
    technical_summary: str
    past_6m_return: Optional[float] = None
    volatility: Optional[str] = None


class StockRecommendation(BaseModel):
    """Top stock recommendation with ranking"""
    rank: int
    stock: StockSignal
    score: float


class SectorAnalysis(BaseModel):
    """Comprehensive sector-level analysis"""
    sector: str
    trend: str  # Bullish, Neutral, Bearish
    planetary_influence: str
    ai_insights: str
    stocks_in_sector: List[StockSignal]
    confidence: float


class EnhancedAnalyzeResponse(BaseModel):
    """Enhanced analysis response with recommendations and signals"""
    top_recommendations: List[StockRecommendation]
    sector_analysis: List[SectorAnalysis]
    all_stocks: List[StockSignal]
    overall_sentiment: str
    timestamp: str


# Prediction API Schemas
class PredictRequest(BaseModel):
    """Request schema for market prediction API"""
    date: Optional[str] = None  # ISO format date (YYYY-MM-DD)
    time: Optional[str] = None  # Time in HH:MM:SS format
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None


class LocationInfo(BaseModel):
    """Location information for predictions"""
    latitude: float
    longitude: float
    timezone: str


class PlanetaryTransit(BaseModel):
    """Planetary transit information"""
    planet: str
    longitude: float
    latitude: float
    sign: str
    degree_in_sign: float
    dignity: str
    retrograde: bool
    motion: str
    speed: float
    transit_start: Optional[str] = None  # ISO datetime when planet entered sign
    transit_end: Optional[str] = None  # ISO datetime when planet will leave sign


class KeyInfluence(BaseModel):
    """Key astrological influence"""
    planet: str
    sign: str
    influence_type: str
    strength: str
    description: str


class MarketPrediction(BaseModel):
    """Market prediction results"""
    overall_sentiment: str
    sector_predictions: List[Dict[str, Any]]
    key_influences: List[KeyInfluence]
    ai_analysis: str


class PredictResponse(BaseModel):
    """Response schema for market prediction API"""
    prediction_date: str
    location: LocationInfo
    planetary_transits: List[PlanetaryTransit]
    market_prediction: MarketPrediction
    past_market_data: Optional[List[Dict[str, Any]]] = None
    confidence: float

