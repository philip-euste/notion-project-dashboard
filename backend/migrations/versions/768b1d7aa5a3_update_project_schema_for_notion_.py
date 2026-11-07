"""update project schema for notion properties

Revision ID: 768b1d7aa5a3
Revises: dcb2697999f1
Create Date: 2026-11-07 16:08:58.008086

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "768b1d7aa5a3"
down_revision: Union[str, Sequence[str], None] = "dcb2697999f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add new Notion properties
    op.add_column(
        "projects",
        sa.Column(
            "status_group",
            sa.String(length=30),
            server_default=sa.text("'To-do'"),
            nullable=False,
        ),
    )

    op.add_column(
        "projects",
        sa.Column("next_possible_action", sa.Text(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("potential", sa.String(length=30), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("repository", sa.Text(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column(
            "ide",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "skills",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )

    op.add_column(
        "projects",
        sa.Column(
            "last_updated",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Update existing properties
    op.alter_column(
        "projects",
        "name",
        existing_type=sa.VARCHAR(length=150),
        nullable=True,
    )

    op.alter_column(
        "projects",
        "status",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=50),
        existing_nullable=False,
        server_default=sa.text("'Unknown'"),
    )

    op.alter_column(
        "projects",
        "priority",
        existing_type=sa.VARCHAR(length=20),
        type_=sa.String(length=30),
        existing_nullable=False,
        nullable=True,
    )

    # Remove obsolete properties
    op.drop_column("projects", "description")
    op.drop_column("projects", "due_date")
    op.drop_column("projects", "start_date")

    # Ensure valid Notion Status group/option combinations
    op.create_check_constraint(
        "valid_project_status",
        "projects",
        """
        (
            status_group = 'To-do'
            AND status IN ('Unknown', 'Conceptualized')
        )
        OR
        (
            status_group = 'In progress'
            AND status IN (
                'Make it WORK',
                'Make it RIGHT',
                'Make it FAST',
                'Github Private',
                'Updateable'
            )
        )
        OR
        (
            status_group = 'Complete'
            AND status IN (
                'GitHub Public',
                'File Transferred',
                'Junk'
            )
        )
        """,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove Status constraint first
    op.drop_constraint(
        "valid_project_status",
        "projects",
        type_="check",
    )

    # Restore obsolete properties
    op.add_column(
        "projects",
        sa.Column("start_date", sa.Date(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("due_date", sa.Date(), nullable=True),
    )

    op.add_column(
        "projects",
        sa.Column("description", sa.Text(), nullable=True),
    )

    # Restore original column definitions
    op.alter_column(
        "projects",
        "priority",
        existing_type=sa.String(length=30),
        type_=sa.VARCHAR(length=20),
        existing_nullable=True,
        nullable=False,
    )

    op.alter_column(
        "projects",
        "status",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
        server_default=None,
    )

    op.alter_column(
        "projects",
        "name",
        existing_type=sa.VARCHAR(length=150),
        nullable=False,
    )

    # Remove new Notion properties
    op.drop_column("projects", "last_updated")
    op.drop_column("projects", "skills")
    op.drop_column("projects", "ide")
    op.drop_column("projects", "repository")
    op.drop_column("projects", "potential")
    op.drop_column("projects", "next_possible_action")
    op.drop_column("projects", "status_group")