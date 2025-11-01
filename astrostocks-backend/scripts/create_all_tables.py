#!/usr/bin/env python3
"""
Create all missing tables from migration files
"""
from sqlalchemy import create_engine, text

# Database URL from backend
DATABASE_URL = 'postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db'

engine = create_engine(DATABASE_URL)

# Combined SQL from all migrations
sql = """
-- Initial migration tables
CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    script_code VARCHAR(20),
    sector VARCHAR(50) NOT NULL,
    sector_id INTEGER,
    past_6m_return FLOAT,
    volatility VARCHAR(20),
    pe_ratio FLOAT,
    price_trend VARCHAR(20),
    news_sentiment VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS ix_stocks_id ON stocks(id);
CREATE INDEX IF NOT EXISTS ix_stocks_symbol ON stocks(symbol);
CREATE INDEX IF NOT EXISTS ix_stocks_sector ON stocks(sector);
CREATE INDEX IF NOT EXISTS ix_stocks_sector_id ON stocks(sector_id);
CREATE INDEX IF NOT EXISTS ix_stocks_script_code ON stocks(script_code);

CREATE TABLE IF NOT EXISTS transits (
    id SERIAL PRIMARY KEY,
    planet VARCHAR(20) NOT NULL,
    sign VARCHAR(20) NOT NULL,
    motion VARCHAR(20),
    status VARCHAR(20),
    date DATE NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_transits_id ON transits(id);
CREATE INDEX IF NOT EXISTS ix_transits_planet ON transits(planet);
CREATE INDEX IF NOT EXISTS ix_transits_date ON transits(date);

CREATE TABLE IF NOT EXISTS sector_predictions (
    id SERIAL PRIMARY KEY,
    sector VARCHAR(50) NOT NULL,
    planetary_influence TEXT,
    trend VARCHAR(20),
    reason TEXT,
    top_stocks JSONB,
    accuracy_estimate FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_sector_predictions_id ON sector_predictions(id);
CREATE INDEX IF NOT EXISTS ix_sector_predictions_sector ON sector_predictions(sector);

CREATE TABLE IF NOT EXISTS market_data_cache (
    symbol VARCHAR(50) PRIMARY KEY,
    current_price FLOAT,
    open_price FLOAT,
    high FLOAT,
    low FLOAT,
    volume FLOAT,
    change_percent FLOAT,
    pe_ratio FLOAT,
    market_cap FLOAT,
    week_52_high FLOAT,
    week_52_low FLOAT,
    sector VARCHAR(100),
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_market_data_cache_symbol ON market_data_cache(symbol);
CREATE INDEX IF NOT EXISTS ix_market_data_cache_sector ON market_data_cache(sector);

-- Sectors table
CREATE TABLE IF NOT EXISTS sectors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    past_6m_return FLOAT,
    past_1y_return FLOAT,
    volatility VARCHAR(20),
    market_cap FLOAT,
    exchange VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS ix_sectors_id ON sectors(id);
CREATE INDEX IF NOT EXISTS ix_sectors_name ON sectors(name);

-- Add foreign key constraint if stocks table exists
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'stocks') THEN
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                       WHERE constraint_name = 'fk_stocks_sector_id') THEN
            ALTER TABLE stocks 
            ADD CONSTRAINT fk_stocks_sector_id 
            FOREIGN KEY (sector_id) REFERENCES sectors(id);
        END IF;
    END IF;
END $$;

-- Cache tables
CREATE TABLE IF NOT EXISTS prediction_cache (
    id SERIAL PRIMARY KEY,
    prediction_date DATE NOT NULL,
    response_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS ix_prediction_cache_id ON prediction_cache(id);
CREATE INDEX IF NOT EXISTS ix_prediction_cache_prediction_date ON prediction_cache(prediction_date);

CREATE TABLE IF NOT EXISTS analyze_cache (
    id SERIAL PRIMARY KEY,
    analysis_date DATE NOT NULL,
    endpoint_type VARCHAR(50) NOT NULL,
    response_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_analyze_cache_date_type UNIQUE (analysis_date, endpoint_type)
);

CREATE INDEX IF NOT EXISTS ix_analyze_cache_id ON analyze_cache(id);
CREATE INDEX IF NOT EXISTS ix_analyze_cache_analysis_date ON analyze_cache(analysis_date);
CREATE INDEX IF NOT EXISTS ix_analyze_cache_endpoint_type ON analyze_cache(endpoint_type);
"""

try:
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print('✅ All tables created successfully!')
except Exception as e:
    print(f'❌ Error: {e}')

