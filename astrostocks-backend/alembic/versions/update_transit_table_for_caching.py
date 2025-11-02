"""update_transit_table_for_caching

Revision ID: transit_update_001
Revises: c4f8e9d2a1b3
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'transit_update_001'
down_revision = 'c4f8e9d2a1b3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to transits table
    op.add_column('transits', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('transits', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('transits', sa.Column('degree_in_sign', sa.Float(), nullable=True))
    op.add_column('transits', sa.Column('retrograde', sa.String(length=10), nullable=True))
    op.add_column('transits', sa.Column('speed', sa.Float(), nullable=True))
    op.add_column('transits', sa.Column('dignity', sa.String(length=20), nullable=True))
    op.add_column('transits', sa.Column('nakshatra', sa.String(length=50), nullable=True))
    op.add_column('transits', sa.Column('transit_start', sa.String(length=100), nullable=True))
    op.add_column('transits', sa.Column('transit_end', sa.String(length=100), nullable=True))
    op.add_column('transits', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('transits', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    
    # Add unique constraint on (date, planet)
    # Check if constraint already exists first
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    constraints = [c['name'] for c in inspector.get_unique_constraints('transits')]
    if 'uq_transit_date_planet' not in constraints:
        op.create_unique_constraint('uq_transit_date_planet', 'transits', ['date', 'planet'])
    
    # Check if index on date already exists
    indexes = [idx['name'] for idx in inspector.get_indexes('transits')]
    if 'ix_transits_date' not in indexes:
        op.create_index('ix_transits_date', 'transits', ['date'], unique=False)


def downgrade() -> None:
    # Drop unique constraint
    op.drop_constraint('uq_transit_date_planet', 'transits', type_='unique')
    
    # Drop columns
    op.drop_column('transits', 'updated_at')
    op.drop_column('transits', 'created_at')
    op.drop_column('transits', 'transit_end')
    op.drop_column('transits', 'transit_start')
    op.drop_column('transits', 'nakshatra')
    op.drop_column('transits', 'dignity')
    op.drop_column('transits', 'speed')
    op.drop_column('transits', 'retrograde')
    op.drop_column('transits', 'degree_in_sign')
    op.drop_column('transits', 'latitude')
    op.drop_column('transits', 'longitude')

