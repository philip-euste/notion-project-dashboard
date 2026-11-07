
from datetime import date, datetime, timezone
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.models import Project


NOTION_VERSION = "2026-03-11"
NOTION_BASE_URL = "https://api.notion.com/v1"

DATA_SOURCE_ID = "368f804e-8948-8008-accb-000ba32ce4b9"


def get_notion_headers() -> dict[str, str]:
    if not settings.notion_api_key:
        raise ValueError("NOTION_API_KEY is missing.")

    return {
        "Authorization": f"Bearer {settings.notion_api_key}",
        "Notion-Version": NOTION_VERSION,
    }


def fetch_notion_projects() -> list[dict[str, Any]]:
    headers = get_notion_headers()
    projects = []
    next_cursor = None

    with httpx.Client(headers=headers, timeout=30.0) as client:
        schema_response = client.get(
            f"{NOTION_BASE_URL}/data_sources/{DATA_SOURCE_ID}"
        )
        schema_response.raise_for_status()

        schema = schema_response.json()

        status_group_map: dict[str, str] = {}

        for group in schema["properties"]["Status"]["status"]["groups"]:
            for option_id in group["option_ids"]:
                status_group_map[option_id] = group["name"]

        while True:
            payload: dict[str, Any] = {"page_size": 100}

            if next_cursor:
                payload["start_cursor"] = next_cursor

            response = client.post(
                f"{NOTION_BASE_URL}/data_sources/{DATA_SOURCE_ID}/query",
                json=payload,
            )
            response.raise_for_status()

            result = response.json()

            projects.extend(
                map_notion_project(page, status_group_map)
                for page in result["results"]
            )

            if not result.get("has_more"):
                break

            next_cursor = result.get("next_cursor")

            if not next_cursor:
                raise ValueError(
                    "Notion returned has_more without a cursor."
                )

    return projects


def map_notion_project(
    page: dict[str, Any],
    status_group_map: dict[str, str],
) -> dict[str, Any]:
    properties = page["properties"]

    title_items = properties["Project name"]["title"]

    name = "".join(
        item["plain_text"] for item in title_items
    ) or None

    status_data = properties["Status"]["status"] or {}

    status = status_data.get("name", "Unknown")
    status_option_id = status_data.get("id")

    status_group = (
        status_group_map.get(status_option_id)
        if isinstance(status_option_id, str)
        else None
    )

    if status_group is None:
        raise ValueError(
            f"Could not determine status group for '{status}'."
        )

    action_items = properties["Next Possible Action"]["rich_text"]

    next_possible_action = "".join(
        item["plain_text"] for item in action_items
    ) or None

    potential_data = properties["Potential"]["select"]
    priority_data = properties["Priority"]["select"]

    potential = potential_data["name"] if potential_data else None
    priority = priority_data["name"] if priority_data else None

    repository = properties["Repository"]["url"]

    ide = [
        item["name"]
        for item in properties["IDE"]["multi_select"]
    ]

    skills = [
        item["name"]
        for item in properties["Skills Used"]["multi_select"]
    ]

    date_data = properties["Locally Last Updated"]["date"]

    last_updated = (
        date.fromisoformat(date_data["start"][:10])
        if date_data
        else None
    )

    return {
        "notion_page_id": page["id"],
        "name": name,
        "status_group": status_group,
        "status": status,
        "next_possible_action": next_possible_action,
        "potential": potential,
        "priority": priority,
        "repository": repository,
        "ide": ide,
        "skills": skills,
        "last_updated": last_updated,
    }


def sync_notion_projects(db: Session) -> dict[str, int]:
    notion_projects = fetch_notion_projects()

    if not notion_projects:
        raise ValueError(
            "Notion returned zero projects. Synchronization aborted "
            "to prevent accidental deletion."
        )

    notion_page_ids = [
        project["notion_page_id"]
        for project in notion_projects
    ]

    existing_projects = db.scalars(
        select(Project).where(
            Project.notion_page_id.in_(notion_page_ids)
        )
    ).all()

    existing_by_notion_id = {
        project.notion_page_id: project
        for project in existing_projects
    }

    stale_projects = db.scalars(
        select(Project).where(
            Project.notion_page_id.is_not(None),
            Project.notion_page_id.not_in(notion_page_ids),
        )
    ).all()

    created = 0
    updated = 0
    deleted = len(stale_projects)

    sync_timestamp = datetime.now(timezone.utc)

    try:
        for notion_project in notion_projects:
            notion_page_id = notion_project["notion_page_id"]

            existing = existing_by_notion_id.get(notion_page_id)

            if existing is None:
                project = Project(**notion_project)
                project.last_synced_at = sync_timestamp

                db.add(project)
                created += 1

            else:
                repository_changed = (
                    existing.repository != notion_project["repository"]
                )

                for field, value in notion_project.items():
                    setattr(existing, field, value)

                if repository_changed:
                    existing.github_pushed_at = None
                    existing.github_last_checked_at = None

                existing.last_synced_at = sync_timestamp
                updated += 1

        for project in stale_projects:
            db.delete(project)

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "total": len(notion_projects),
        "created": created,
        "updated": updated,
        "deleted": deleted,
    }
