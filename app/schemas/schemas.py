from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime


class StockBase(BaseModel):
    symbol: str
    sector: str
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
        description="Optional list of stock data. If not provided, mock data will be used."
    )
    transits: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional planetary transit data. If not provided, mock data will be used."
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

