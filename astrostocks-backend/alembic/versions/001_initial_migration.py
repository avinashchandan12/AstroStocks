"""Initial migration: create stocks, transits, and sector_predictions tables

Revision ID: 001
Revises: 
Create Date: 2025-10-23 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create stocks table
    op.create_table(
        'stocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('sector', sa.String(length=50), nullable=False),
        sa.Column('past_6m_return', sa.Float(), nullable=True),
        sa.Column('volatility', sa.String(length=20), nullable=True),
        sa.Column('pe_ratio', sa.Float(), nullable=True),
        sa.Column('price_trend', sa.String(length=20), nullable=True),
        sa.Column('news_sentiment', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)
    op.create_index(op.f('ix_stocks_symbol'), 'stocks', ['symbol'], unique=False)
    op.create_index(op.f('ix_stocks_sector'), 'stocks', ['sector'], unique=False)

    # Create transits table
    op.create_table(
        'transits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('planet', sa.String(length=20), nullable=False),
        sa.Column('sign', sa.String(length=20), nullable=False),
        sa.Column('motion', sa.String(length=20), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transits_id'), 'transits', ['id'], unique=False)
    op.create_index(op.f('ix_transits_planet'), 'transits', ['planet'], unique=False)
    op.create_index(op.f('ix_transits_date'), 'transits', ['date'], unique=False)

    # Create sector_predictions table
    op.create_table(
        'sector_predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sector', sa.String(length=50), nullable=False),
        sa.Column('planetary_influence', sa.Text(), nullable=True),
        sa.Column('trend', sa.String(length=20), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('top_stocks', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('accuracy_estimate', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sector_predictions_id'), 'sector_predictions', ['id'], unique=False)
    op.create_index(op.f('ix_sector_predictions_sector'), 'sector_predictions', ['sector'], unique=False)


def downgrade() -> None:
    # Drop sector_predictions table
    op.drop_index(op.f('ix_sector_predictions_sector'), table_name='sector_predictions')
    op.drop_index(op.f('ix_sector_predictions_id'), table_name='sector_predictions')
    op.drop_table('sector_predictions')

    # Drop transits table
    op.drop_index(op.f('ix_transits_date'), table_name='transits')
    op.drop_index(op.f('ix_transits_planet'), table_name='transits')
    op.drop_index(op.f('ix_transits_id'), table_name='transits')
    op.drop_table('transits')

    # Drop stocks table
    op.drop_index(op.f('ix_stocks_sector'), table_name='stocks')
    op.drop_index(op.f('ix_stocks_symbol'), table_name='stocks')
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')

