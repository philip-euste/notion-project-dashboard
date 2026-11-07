from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

import httpx

from app.core.config import settings
from app.database.models import Project


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

        if parsed.hostname not in {"github.com", "www.github.com"}:
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


def get_retry_delay(response: httpx.Response) -> timedelta:
    reset_timestamp = response.headers.get("X-RateLimit-Reset")

    if reset_timestamp:
        try:
            reset_at = datetime.fromtimestamp(
                int(reset_timestamp),
                tz=timezone.utc,
            )

            delay = reset_at - datetime.now(timezone.utc)

            return max(
                RETRY_DELAY,
                delay + timedelta(seconds=5),
            )

        except (ValueError, OverflowError):
            pass

    return RETRY_DELAY


def refresh_project_github_data(
    project: Project,
    client: httpx.Client,
) -> tuple[str, timedelta | None]:
    now = datetime.now(timezone.utc)

    if not project.repository:
        changed = (
            project.github_pushed_at is not None
            or project.github_last_checked_at is not None
        )

        project.github_pushed_at = None
        project.github_last_checked_at = None

        return ("cleared" if changed else "skipped"), None

    if (
        project.github_last_checked_at
        and now - project.github_last_checked_at < CACHE_DURATION
    ):
        return "cached", None

    repository = parse_github_repository(project.repository)

    if repository is None:
        project.github_pushed_at = None
        project.github_last_checked_at = now

        return "invalid", None

    owner, repository_name = repository

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository_name}"
    )

    try:
        response = client.get(url)

        if (
            response.status_code == 429
            or (
                response.status_code == 403
                and response.headers.get("X-RateLimit-Remaining") == "0"
            )
        ):
            delay = get_retry_delay(response)

            project.github_last_checked_at = (
                now - CACHE_DURATION + delay
            )

            return "rate_limited", delay

        response.raise_for_status()

        data = response.json()
        pushed_at = data.get("pushed_at")

        if not isinstance(pushed_at, str):
            raise ValueError(
                "GitHub response has no valid pushed_at value."
            )

        parsed_timestamp = datetime.fromisoformat(
            pushed_at.replace("Z", "+00:00")
        )

        if parsed_timestamp.tzinfo is None:
            parsed_timestamp = parsed_timestamp.replace(
                tzinfo=timezone.utc
            )

        project.github_pushed_at = parsed_timestamp
        project.github_last_checked_at = now

        return "updated", None

    except (httpx.HTTPError, ValueError, KeyError, TypeError, AttributeError):
        # Retry failed requests after 15 minutes instead of
        # repeatedly calling GitHub on every dashboard refresh.
        project.github_last_checked_at = (
            now - CACHE_DURATION + RETRY_DELAY
        )

        return "failed", None


def refresh_github_projects(
    projects: Sequence[Project],
) -> dict[str, int]:
    now = datetime.now(timezone.utc)

    projects_to_check = [
        project
        for project in projects
        if (
            not project.github_last_checked_at
            or now - project.github_last_checked_at >= CACHE_DURATION
        )
    ]

    results = {
        "total": len(projects),
        "checked": 0,
        "updated": 0,
        "failed": 0,
        "invalid": 0,
        "cleared": 0,
        "cached": len(projects) - len(projects_to_check),
        "deferred": 0,
    }

    if not projects_to_check:
        return results

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Notion-Project-Dashboard",
    }

    if settings.github_token:
        headers["Authorization"] = (
            f"Bearer {settings.github_token}"
        )

    with httpx.Client(
        timeout=10.0,
        headers=headers,
    ) as client:
        for index, project in enumerate(projects_to_check):
            status, retry_delay = refresh_project_github_data(
                project,
                client,
            )

            if status == "rate_limited":
                results["failed"] += 1

                remaining_projects = projects_to_check[index + 1:]

                retry_at = (
                    now - CACHE_DURATION + retry_delay
                    if retry_delay
                    else now - CACHE_DURATION + RETRY_DELAY
                )

                for remaining_project in remaining_projects:
                    remaining_project.github_last_checked_at = retry_at

                results["deferred"] += len(remaining_projects)
                break

            if status == "cached":
                results["cached"] += 1

            elif status == "updated":
                results["updated"] += 1
                results["checked"] += 1

            elif status == "failed":
                results["failed"] += 1
                results["checked"] += 1

            elif status == "invalid":
                results["invalid"] += 1
                results["checked"] += 1

            elif status == "cleared":
                results["cleared"] += 1
                results["checked"] += 1

            elif status == "skipped":
                results["checked"] += 1

    return results