"""add_prediction_and_analyze_cache

Revision ID: 89c0faf56dc7
Revises: ba31a63ea719
Create Date: 2025-11-01 15:14:35.097997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c0faf56dc7'
down_revision = 'ba31a63ea719'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create prediction_cache table
    op.create_table(
        'prediction_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('prediction_date', sa.Date(), nullable=False),
        sa.Column('response_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for prediction_cache
    op.create_index('ix_prediction_cache_id', 'prediction_cache', ['id'], unique=False)
    op.create_index('ix_prediction_cache_prediction_date', 'prediction_cache', ['prediction_date'], unique=False)
    
    # Create analyze_cache table
    op.create_table(
        'analyze_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_date', sa.Date(), nullable=False),
        sa.Column('endpoint_type', sa.String(length=50), nullable=False),
        sa.Column('response_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('analysis_date', 'endpoint_type', name='uq_analyze_cache_date_type')
    )
    
    # Create indexes for analyze_cache
    op.create_index('ix_analyze_cache_id', 'analyze_cache', ['id'], unique=False)
    op.create_index('ix_analyze_cache_analysis_date', 'analyze_cache', ['analysis_date'], unique=False)
    op.create_index('ix_analyze_cache_endpoint_type', 'analyze_cache', ['endpoint_type'], unique=False)


def downgrade() -> None:
    # Drop indexes for analyze_cache
    op.drop_index('ix_analyze_cache_endpoint_type', table_name='analyze_cache')
    op.drop_index('ix_analyze_cache_analysis_date', table_name='analyze_cache')
    op.drop_index('ix_analyze_cache_id', table_name='analyze_cache')
    
    # Drop analyze_cache table
    op.drop_table('analyze_cache')
    
    # Drop indexes for prediction_cache
    op.drop_index('ix_prediction_cache_prediction_date', table_name='prediction_cache')
    op.drop_index('ix_prediction_cache_id', table_name='prediction_cache')
    
    # Drop prediction_cache table
    op.drop_table('prediction_cache')

