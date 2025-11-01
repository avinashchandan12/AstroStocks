"""add_script_code_to_stocks

Revision ID: ba31a63ea719
Revises: 2a3cdd88496f
Create Date: 2025-11-01 14:54:21.014778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba31a63ea719'
down_revision = '2a3cdd88496f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add script_code column to stocks table
    op.add_column('stocks', sa.Column('script_code', sa.String(length=20), nullable=True))
    
    # Create index for script_code
    op.create_index('ix_stocks_script_code', 'stocks', ['script_code'], unique=False)


def downgrade() -> None:
    # Drop index
    op.drop_index('ix_stocks_script_code', table_name='stocks')
    
    # Drop script_code column
    op.drop_column('stocks', 'script_code')

