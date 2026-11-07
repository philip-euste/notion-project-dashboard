from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None

    status: str = "not_started"
    priority: str = "medium"

    start_date: date | None = None
    due_date: date | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None

    status: str | None = None
    priority: str | None = None

    start_date: date | None = None
    due_date: date | None = None


class ProjectResponse(ProjectBase):
    id: UUID
    notion_page_id: str | None
    last_synced_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)