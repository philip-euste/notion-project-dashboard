"""add GitHub sync scheduling columns

Revision ID: eb128c10606a
Revises: 5268d353e74c
Create Date: 2026-11-08
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eb128c10606a"
down_revision: Union[str, Sequence[str], None] = "5268d353e74c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "projects",
        sa.Column(
            "github_next_check_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "github_notion_synced_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("projects", "github_notion_synced_at")
    op.drop_column("projects", "github_next_check_at")