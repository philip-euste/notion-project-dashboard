
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

import httpx

from app.database.models import Project
from collections.abc import Sequence

GITHUB_API_URL = "https://api.github.com"

CACHE_DURATION = timedelta(hours=6)
RETRY_DELAY = timedelta(minutes=15)


def parse_github_repository(
    repository_url: str | None,
) -> tuple[str, str] | None:
    if not repository_url:
        return None

    try:
        parsed = urlsplit(repository_url.strip())

        if parsed.hostname != "github.com":
            return None

        parts = [
            part
            for part in parsed.path.strip("/").split("/")
            if part
        ]

        if len(parts) < 2:
            return None

        owner = parts[0]
        repository = parts[1]

        if repository.endswith(".git"):
            repository = repository[:-4]

        if not owner or not repository:
            return None

        return owner, repository

    except (ValueError, AttributeError):
        return None


def refresh_project_github_data(
    project: Project,
    client: httpx.Client,
) -> bool:
    now = datetime.now(timezone.utc)

    if not project.repository:
        changed = (
            project.github_pushed_at is not None
            or project.github_last_checked_at is not None
        )

        project.github_pushed_at = None
        project.github_last_checked_at = None

        return changed

    if (
        project.github_last_checked_at
        and now - project.github_last_checked_at < CACHE_DURATION
    ):
        return False

    repository = parse_github_repository(project.repository)

    if repository is None:
        project.github_pushed_at = None
        project.github_last_checked_at = now
        return True

    owner, repository_name = repository

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository_name}"
    )

    try:
        response = client.get(url)
        response.raise_for_status()

        data = response.json()
        pushed_at = data.get("pushed_at")

        if not pushed_at:
            raise ValueError("GitHub response has no pushed_at value.")

        parsed_timestamp = datetime.fromisoformat(
            pushed_at.replace("Z", "+00:00")
        )

        if parsed_timestamp.tzinfo is None:
            parsed_timestamp = parsed_timestamp.replace(
                tzinfo=timezone.utc
            )

        project.github_pushed_at = parsed_timestamp
        project.github_last_checked_at = now

        return True

    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        # Retry failed requests after 15 minutes instead of
        # repeatedly calling GitHub on every dashboard refresh.
        project.github_last_checked_at = (
            now - CACHE_DURATION + RETRY_DELAY
        )

        return True


def refresh_github_projects(projects: Sequence[Project]) -> None:
    projects_to_check = [
        project
        for project in projects
        if (
            not project.github_last_checked_at
            or datetime.now(timezone.utc)
            - project.github_last_checked_at
            >= CACHE_DURATION
        )
    ]

    if not projects_to_check:
        return

    with httpx.Client(
        timeout=10.0,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Notion-Project-Dashboard",
        },
    ) as client:
        for project in projects_to_check:
            refresh_project_github_data(project, client)
