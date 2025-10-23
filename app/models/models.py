from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database.config import Base


class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    sector = Column(String(50), nullable=False, index=True)
    past_6m_return = Column(Float)
    volatility = Column(String(20))
    pe_ratio = Column(Float)
    price_trend = Column(String(20))
    news_sentiment = Column(String(50))


class Transit(Base):
    __tablename__ = "transits"
    
    id = Column(Integer, primary_key=True, index=True)
    planet = Column(String(20), nullable=False, index=True)
    sign = Column(String(20), nullable=False)
    motion = Column(String(20))
    status = Column(String(20))
    date = Column(Date, nullable=False, index=True)


class SectorPrediction(Base):
    __tablename__ = "sector_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    sector = Column(String(50), nullable=False, index=True)
    planetary_influence = Column(Text)
    trend = Column(String(20))
    reason = Column(Text)
    top_stocks = Column(JSON)
    accuracy_estimate = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MarketDataCache(Base):
    __tablename__ = "market_data_cache"
    
    symbol = Column(String(50), primary_key=True, index=True)
    current_price = Column(Float)
    open_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    change_percent = Column(Float)
    pe_ratio = Column(Float)
    market_cap = Column(Float)
    week_52_high = Column(Float)
    week_52_low = Column(Float)
    sector = Column(String(100), index=True)
    cached_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

