#!/usr/bin/env python3
"""
Create cache tables manually if Alembic migrations haven't been run
"""
from sqlalchemy import create_engine, text

# Database URL from backend
DATABASE_URL = 'postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db'

engine = create_engine(DATABASE_URL)

sql = """
-- Create prediction_cache table
CREATE TABLE IF NOT EXISTS prediction_cache (
    id SERIAL PRIMARY KEY,
    prediction_date DATE NOT NULL,
    response_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for prediction_cache
CREATE INDEX IF NOT EXISTS ix_prediction_cache_id ON prediction_cache(id);
CREATE INDEX IF NOT EXISTS ix_prediction_cache_prediction_date ON prediction_cache(prediction_date);

-- Create analyze_cache table
CREATE TABLE IF NOT EXISTS analyze_cache (
    id SERIAL PRIMARY KEY,
    analysis_date DATE NOT NULL,
    endpoint_type VARCHAR(50) NOT NULL,
    response_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_analyze_cache_date_type UNIQUE (analysis_date, endpoint_type)
);

-- Create indexes for analyze_cache
CREATE INDEX IF NOT EXISTS ix_analyze_cache_id ON analyze_cache(id);
CREATE INDEX IF NOT EXISTS ix_analyze_cache_analysis_date ON analyze_cache(analysis_date);
CREATE INDEX IF NOT EXISTS ix_analyze_cache_endpoint_type ON analyze_cache(endpoint_type);
"""

try:
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print('✅ Cache tables created successfully!')
except Exception as e:
    print(f'❌ Error: {e}')

