"""add market data cache table

Revision ID: 002
Revises: 001
Create Date: 2025-10-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create market_data_cache table
    op.create_table(
        'market_data_cache',
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('current_price', sa.Float(), nullable=True),
        sa.Column('open_price', sa.Float(), nullable=True),
        sa.Column('high', sa.Float(), nullable=True),
        sa.Column('low', sa.Float(), nullable=True),
        sa.Column('volume', sa.Float(), nullable=True),
        sa.Column('change_percent', sa.Float(), nullable=True),
        sa.Column('pe_ratio', sa.Float(), nullable=True),
        sa.Column('market_cap', sa.Float(), nullable=True),
        sa.Column('week_52_high', sa.Float(), nullable=True),
        sa.Column('week_52_low', sa.Float(), nullable=True),
        sa.Column('sector', sa.String(length=100), nullable=True),
        sa.Column('cached_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('symbol')
    )
    
    # Create indexes
    op.create_index('ix_market_data_cache_symbol', 'market_data_cache', ['symbol'], unique=False)
    op.create_index('ix_market_data_cache_sector', 'market_data_cache', ['sector'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_market_data_cache_sector', table_name='market_data_cache')
    op.drop_index('ix_market_data_cache_symbol', table_name='market_data_cache')
    
    # Drop table
    op.drop_table('market_data_cache')

