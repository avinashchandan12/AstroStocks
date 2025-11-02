from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.config import Base


class Sector(Base):
    __tablename__ = "sectors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    
    # Sector performance metrics
    past_6m_return = Column(Float)  # Average 6-month return for sector
    past_1y_return = Column(Float)  # Average 1-year return for sector
    volatility = Column(String(20))  # High, Medium, Low
    market_cap = Column(Float)  # Total market cap of sector
    
    # Additional metadata
    exchange = Column(String(50))  # NSE, BSE, Both
    country = Column(String(50), default='India')  # Country of operation
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    stocks = relationship("Stock", back_populates="sector_relation")


class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    script_code = Column(String(20), index=True)  # Exchange script code (e.g., NSE, BSE)
    
    # Keep sector as string for backward compatibility, add FK
    sector = Column(String(50), nullable=False, index=True)  # Legacy column
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=True, index=True)  # Will be made required later
    
    past_6m_return = Column(Float)
    volatility = Column(String(20))
    pe_ratio = Column(Float)
    price_trend = Column(String(20))
    news_sentiment = Column(String(50))
    
    # Relationships
    sector_relation = relationship("Sector", back_populates="stocks")


class Transit(Base):
    __tablename__ = "transits"
    
    id = Column(Integer, primary_key=True, index=True)
    planet = Column(String(20), nullable=False, index=True)
    sign = Column(String(20), nullable=False)
    motion = Column(String(20))
    status = Column(String(20))
    date = Column(Date, nullable=False, index=True)
    
    # Additional transit data for full planetary transit information
    longitude = Column(Float)
    latitude = Column(Float)
    degree_in_sign = Column(Float)
    retrograde = Column(String(10))  # Store as string for boolean representation
    speed = Column(Float)
    dignity = Column(String(20))
    nakshatra = Column(String(50))
    transit_start = Column(String(100))  # ISO datetime string
    transit_end = Column(String(100))  # ISO datetime string
    
    # Metadata for caching
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Unique constraint: one transit record per planet per date
    __table_args__ = (
        UniqueConstraint('date', 'planet', name='uq_transit_date_planet'),
    )


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


class PredictionCache(Base):
    """Cache for /predict endpoint responses"""
    __tablename__ = "prediction_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_date = Column(Date, nullable=False, index=True)
    
    # Store full prediction response as JSON
    response_data = Column(JSON, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AnalyzeCache(Base):
    """Cache for /analyze and /analyze/enhanced endpoint responses"""
    __tablename__ = "analyze_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Analysis date (primary lookup key)
    analysis_date = Column(Date, nullable=False, index=True)
    
    # Endpoint type
    endpoint_type = Column(String(50), nullable=False, index=True)  # 'basic' or 'enhanced'
    
    # Store full analysis response as JSON
    response_data = Column(JSON, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Unique constraint: one analysis per date per type
    __table_args__ = (
        UniqueConstraint('analysis_date', 'endpoint_type', name='uq_analyze_cache_date_type'),
    )


class SectorArchive(Base):
    """Archive table for old sector predictions when hard refresh is performed"""
    __tablename__ = "sector_archive"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Original prediction data
    sector = Column(String(50), nullable=False, index=True)
    planetary_influence = Column(Text)
    trend = Column(String(20))
    reason = Column(Text)
    top_stocks = Column(JSON)
    accuracy_estimate = Column(Float)
    sector_id = Column(Integer, nullable=True, index=True)
    sector_name = Column(String(100))
    confidence = Column(String(20))
    ai_insights = Column(Text)
    transit_start = Column(String(100))
    transit_end = Column(String(100))
    
    # Archive metadata
    original_created_at = Column(DateTime(timezone=True))  # When the original prediction was created
    archived_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    archive_date = Column(Date, nullable=False, index=True)  # The date this prediction was for

