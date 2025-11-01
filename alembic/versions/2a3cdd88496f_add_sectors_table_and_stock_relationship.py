"""add_sectors_table_and_stock_relationship

Revision ID: 2a3cdd88496f
Revises: 002
Create Date: 2025-11-01 14:16:42.200781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a3cdd88496f'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sectors table
    op.create_table(
        'sectors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('past_6m_return', sa.Float(), nullable=True),
        sa.Column('past_1y_return', sa.Float(), nullable=True),
        sa.Column('volatility', sa.String(length=20), nullable=True),
        sa.Column('market_cap', sa.Float(), nullable=True),
        sa.Column('exchange', sa.String(length=50), nullable=True),
        sa.Column('country', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create indexes for sectors
    op.create_index('ix_sectors_id', 'sectors', ['id'], unique=False)
    op.create_index('ix_sectors_name', 'sectors', ['name'], unique=False)
    
    # Add sector_id column to stocks table
    op.add_column('stocks', sa.Column('sector_id', sa.Integer(), nullable=True))
    
    # Create index for sector_id
    op.create_index('ix_stocks_sector_id', 'stocks', ['sector_id'], unique=False)
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_stocks_sector_id',
        'stocks', 'sectors',
        ['sector_id'], ['id']
    )
    
    # Note: We keep the existing 'sector' string column for backward compatibility


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('fk_stocks_sector_id', 'stocks', type_='foreignkey')
    
    # Drop index
    op.drop_index('ix_stocks_sector_id', table_name='stocks')
    
    # Drop sector_id column
    op.drop_column('stocks', 'sector_id')
    
    # Drop indexes for sectors
    op.drop_index('ix_sectors_name', table_name='sectors')
    op.drop_index('ix_sectors_id', table_name='sectors')
    
    # Drop sectors table
    op.drop_table('sectors')

