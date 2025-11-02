"""add_sector_archive_table

Revision ID: c4f8e9d2a1b3
Revises: 89c0faf56dc7
Create Date: 2025-11-01 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c4f8e9d2a1b3'
down_revision = '89c0faf56dc7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sector_archive table
    op.create_table(
        'sector_archive',
        sa.Column('id', sa.Integer(), nullable=False),
        # Original prediction data
        sa.Column('sector', sa.String(length=50), nullable=False),
        sa.Column('planetary_influence', sa.Text(), nullable=True),
        sa.Column('trend', sa.String(length=20), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('top_stocks', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('accuracy_estimate', sa.Float(), nullable=True),
        sa.Column('sector_id', sa.Integer(), nullable=True),
        sa.Column('sector_name', sa.String(length=100), nullable=True),
        sa.Column('confidence', sa.String(length=20), nullable=True),
        sa.Column('ai_insights', sa.Text(), nullable=True),
        sa.Column('transit_start', sa.String(length=100), nullable=True),
        sa.Column('transit_end', sa.String(length=100), nullable=True),
        # Archive metadata
        sa.Column('original_created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('archived_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('archive_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for sector_archive
    op.create_index('ix_sector_archive_id', 'sector_archive', ['id'], unique=False)
    op.create_index('ix_sector_archive_sector', 'sector_archive', ['sector'], unique=False)
    op.create_index('ix_sector_archive_sector_id', 'sector_archive', ['sector_id'], unique=False)
    op.create_index('ix_sector_archive_archived_at', 'sector_archive', ['archived_at'], unique=False)
    op.create_index('ix_sector_archive_archive_date', 'sector_archive', ['archive_date'], unique=False)


def downgrade() -> None:
    # Drop indexes for sector_archive
    op.drop_index('ix_sector_archive_archive_date', table_name='sector_archive')
    op.drop_index('ix_sector_archive_archived_at', table_name='sector_archive')
    op.drop_index('ix_sector_archive_sector_id', table_name='sector_archive')
    op.drop_index('ix_sector_archive_sector', table_name='sector_archive')
    op.drop_index('ix_sector_archive_id', table_name='sector_archive')
    
    # Drop sector_archive table
    op.drop_table('sector_archive')

