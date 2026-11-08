
import uuid

from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Project(Base):
    __tablename__ = "projects"

    __table_args__ = (
        CheckConstraint(
            """
            (status_group = 'To-do' AND status IN ('Unknown', 'Conceptualized'))
            OR
            (status_group = 'In progress' AND status IN (
                'Make it WORK',
                'Make it RIGHT',
                'Make it FAST',
                'Github Private',
                'Updateable'
            ))
            OR
            (status_group = 'Complete' AND status IN (
                'GitHub Public',
                'File Transferred',
                'Junk'
            ))
            """,
            name="valid_project_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    notion_page_id: Mapped[str | None] = mapped_column(
        String(36),
        unique=True,
        nullable=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    status_group: Mapped[str] = mapped_column(
        String(30),
        default="To-do",
        server_default=text("'To-do'"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Unknown",
        server_default=text("'Unknown'"),
        nullable=False,
    )

    next_possible_action: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    potential: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    priority: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    repository: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ide: Mapped[list[str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    skills: Mapped[list[str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Date maintained by Notion.
    last_updated: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # GitHub synchronization data.
    github_pushed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    github_last_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    github_next_check_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    github_notion_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Internal synchronization timestamps.
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @property
    def displayed_last_updated(self) -> date | None:
        dates = []

        if self.last_updated:
            dates.append(self.last_updated)

        if self.github_pushed_at:
            dates.append(self.github_pushed_at.date())

        return max(dates) if dates else None
