from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


# Allowed Notion values

StatusGroup = Literal[
    "To-do",
    "In progress",
    "Complete",
]

ProjectStatus = Literal[
    "Unknown",
    "Conceptualized",
    "Make it WORK",
    "Make it RIGHT",
    "Make it FAST",
    "Github Private",
    "Updateable",
    "GitHub Public",
    "File Transferred",
    "Junk",
]

ProjectPotential = Literal[
    "Minor",
    "Major",
    "Not Mine",
    "Scalable",
    "Junk",
]

ProjectPriority = Literal[
    "Finished",
    "GitHubable",
    "High",
    "Medium",
    "Low",
    "Impossible",
]


# Status group and option validation

STATUS_OPTIONS = {
    "To-do": {"Unknown", "Conceptualized"},
    "In progress": {
        "Make it WORK",
        "Make it RIGHT",
        "Make it FAST",
        "Github Private",
        "Updateable",
    },
    "Complete": {
        "GitHub Public",
        "File Transferred",
        "Junk",
    },
}


def validate_status_pair(group: str, status: str) -> None:
    if status not in STATUS_OPTIONS[group]:
        raise ValueError(
            f"Status '{status}' does not belong to group '{group}'."
        )


# Base project schema

class ProjectBase(BaseModel):
    name: str | None = Field(default=None, max_length=150)

    status_group: StatusGroup = "To-do"
    status: ProjectStatus = "Unknown"

    next_possible_action: str | None = None
    potential: ProjectPotential | None = None
    priority: ProjectPriority | None = None

    repository: str | None = None
    ide: list[str] | None = None
    skills: list[str] | None = None

    last_updated: date | None = None

    @model_validator(mode="after")
    def validate_status(self):
        validate_status_pair(self.status_group, self.status)
        return self


# Create project

class ProjectCreate(ProjectBase):
    pass


# Update project

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=150)

    status_group: StatusGroup | None = None
    status: ProjectStatus | None = None

    next_possible_action: str | None = None
    potential: ProjectPotential | None = None
    priority: ProjectPriority | None = None

    repository: str | None = None
    ide: list[str] | None = None
    skills: list[str] | None = None

    last_updated: date | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if "status_group" in self.model_fields_set:
            if self.status_group is None:
                raise ValueError("status_group cannot be null")

        if "status" in self.model_fields_set:
            if self.status is None:
                raise ValueError("status cannot be null")

        if (
            "status_group" in self.model_fields_set
            and "status" in self.model_fields_set
            and self.status_group is not None
            and self.status is not None
        ):
            validate_status_pair(self.status_group, self.status)

        return self


# API response

class ProjectResponse(ProjectBase):
    id: UUID
    notion_page_id: str | None
    last_synced_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)