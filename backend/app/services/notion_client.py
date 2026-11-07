
from datetime import date
from typing import Any

import httpx

from app.core.config import settings


NOTION_VERSION = "2026-03-11"
NOTION_BASE_URL = "https://api.notion.com/v1"

DATA_SOURCE_ID = "368f804e-8948-8008-accb-000ba32ce4b9"


def get_notion_headers() -> dict[str, str]:
    if not settings.notion_api_key:
        raise ValueError("NOTION_API_KEY is missing.")

    return {
        "Authorization": f"Bearer {settings.notion_api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def build_notion_properties(
    project: dict[str, Any],
) -> dict[str, Any]:
    name = project.get("name")
    action = project.get("next_possible_action")
    last_updated = project.get("last_updated")

    if isinstance(last_updated, date):
        last_updated = last_updated.isoformat()

    return {
        "Project name": {
            "title": (
                [{"text": {"content": name}}]
                if name
                else []
            )
        },
        "Status": {
            "status": {
                "name": project["status"]
            }
        },
        "Skills Used": {
            "multi_select": [
                {"name": skill}
                for skill in project.get("skills") or []
            ]
        },
        "Next Possible Action": {
            "rich_text": (
                [{"text": {"content": action}}]
                if action
                else []
            )
        },
        "Priority": {
            "select": (
                {"name": project["priority"]}
                if project.get("priority")
                else None
            )
        },
        "Potential": {
            "select": (
                {"name": project["potential"]}
                if project.get("potential")
                else None
            )
        },
        "Repository": {
            "url": project.get("repository")
        },
        "Last Updated": {
            "date": (
                {"start": last_updated}
                if last_updated
                else None
            )
        },
        "IDE": {
            "multi_select": [
                {"name": ide}
                for ide in project.get("ide") or []
            ]
        },
    }


def create_notion_page(project: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "parent": {
            "data_source_id": DATA_SOURCE_ID
        },
        "properties": build_notion_properties(project),
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            f"{NOTION_BASE_URL}/pages",
            headers=get_notion_headers(),
            json=payload,
        )
        response.raise_for_status()

        return response.json()


def update_notion_page(
    page_id: str,
    project: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "properties": build_notion_properties(project)
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.patch(
            f"{NOTION_BASE_URL}/pages/{page_id}",
            headers=get_notion_headers(),
            json=payload,
        )
        response.raise_for_status()

        return response.json()


def archive_notion_page(page_id: str) -> dict[str, Any]:
    with httpx.Client(timeout=30.0) as client:
        response = client.patch(
            f"{NOTION_BASE_URL}/pages/{page_id}",
            headers=get_notion_headers(),
            json={"in_trash": True},
        )
        response.raise_for_status()

        return response.json()
