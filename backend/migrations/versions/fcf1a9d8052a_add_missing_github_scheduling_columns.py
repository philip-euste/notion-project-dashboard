"""add missing GitHub scheduling columns

Revision ID: fcf1a9d8052a
Revises: eb128c10606a
Create Date: 2026-11-08 11:14:31.892234
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fcf1a9d8052a"
down_revision: Union[str, Sequence[str], None] = "eb128c10606a"
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

    op.execute(
        """
        UPDATE projects
        SET github_next_check_at = github_last_checked_at
            + INTERVAL '6 hours'
        WHERE github_last_checked_at IS NOT NULL
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("projects", "github_notion_synced_at")
    op.drop_column("projects", "github_next_check_at")