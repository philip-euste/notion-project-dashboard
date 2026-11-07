"""add GitHub synchronization fields

Revision ID: 6155ac2cd1a6
Revises: a402e5c639db
Create Date: 2026-11-07 20:20:44.832223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6155ac2cd1a6'
down_revision: Union[str, Sequence[str], None] = 'a402e5c639db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'projects',
        sa.Column('github_pushed_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        'projects',
        sa.Column('github_last_checked_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('projects', 'github_last_checked_at')
    op.drop_column('projects', 'github_pushed_at')