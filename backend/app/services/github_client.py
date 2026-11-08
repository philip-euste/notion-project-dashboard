
from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

import httpx

from app.core.config import settings
from app.database.models import Project


GITHUB_API_URL = "https://api.github.com"

CACHE_DURATION = timedelta(hours=6)
RETRY_DELAY = timedelta(minutes=15)
BATCH_SIZE = 40


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
    retry_after = response.headers.get("Retry-After")

    if retry_after:
        try:
            return max(
                RETRY_DELAY,
                timedelta(seconds=float(retry_after)),
            )

        except (ValueError, OverflowError):
            pass

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


def is_rate_limited(response: httpx.Response) -> bool:
    if response.status_code == 429:
        return True

    if response.status_code != 403:
        return False

    remaining = response.headers.get("X-RateLimit-Remaining")

    if remaining == "0":
        return True

    if response.headers.get("Retry-After"):
        return True

    return "secondary rate limit" in response.text.lower()


def refresh_project_github_data(
    project: Project,
    client: httpx.Client,
) -> tuple[str, timedelta | None]:
    now = datetime.now(timezone.utc)

    repository = parse_github_repository(project.repository)

    if repository is None:
        project.github_last_checked_at = now
        project.github_next_check_at = now + CACHE_DURATION

        return "invalid", None

    owner, repository_name = repository

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository_name}"
    )

    try:
        response = client.get(url)

        if is_rate_limited(response):
            delay = get_retry_delay(response)

            project.github_last_checked_at = now
            project.github_next_check_at = now + delay

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

        timestamp_changed = (
            project.github_pushed_at != parsed_timestamp
        )

        project.github_pushed_at = parsed_timestamp
        project.github_last_checked_at = now
        project.github_next_check_at = now + CACHE_DURATION

        if timestamp_changed:
            project.github_notion_synced_at = None

        return "updated", None

    except (
        httpx.HTTPError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
    ):
        project.github_last_checked_at = now
        project.github_next_check_at = now + RETRY_DELAY

        return "failed", None


def refresh_github_projects(
    projects: Sequence[Project],
) -> dict[str, int]:
    now = datetime.now(timezone.utc)

    results = {
        "total": len(projects),
        "eligible": 0,
        "checked": 0,
        "updated": 0,
        "failed": 0,
        "invalid": 0,
        "cleared": 0,
        "cached": 0,
        "deferred": 0,
        "no_repository": 0,
    }

    projects_with_repositories = []

    for project in projects:
        if not project.repository:
            changed = (
                project.github_pushed_at is not None
                or project.github_last_checked_at is not None
                or project.github_next_check_at is not None
                or project.github_notion_synced_at is not None
            )

            if changed:
                project.github_pushed_at = None
                project.github_last_checked_at = None
                project.github_next_check_at = None
                project.github_notion_synced_at = None

                results["cleared"] += 1
            else:
                results["no_repository"] += 1

            continue

        projects_with_repositories.append(project)

    eligible_projects = [
        project
        for project in projects_with_repositories
        if (
            project.github_next_check_at is None
            or project.github_next_check_at <= now
        )
    ]

    results["eligible"] = len(eligible_projects)
    results["cached"] = (
        len(projects_with_repositories) - len(eligible_projects)
    )

    eligible_projects.sort(
        key=lambda project: (
            project.github_last_checked_at is not None,
            project.github_last_checked_at
            or datetime.min.replace(tzinfo=timezone.utc),
            str(project.id),
        )
    )

    projects_to_check = eligible_projects[:BATCH_SIZE]
    remaining_projects = eligible_projects[BATCH_SIZE:]

    results["deferred"] = len(remaining_projects)

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
                results["checked"] += 1

                retry_at = (
                    now + retry_delay
                    if retry_delay
                    else now + RETRY_DELAY
                )

                unprocessed_projects = (
                    projects_to_check[index + 1:]
                    + remaining_projects
                )

                for remaining_project in unprocessed_projects:
                    remaining_project.github_next_check_at = retry_at

                results["deferred"] = len(unprocessed_projects)
                break

            if status == "updated":
                results["updated"] += 1
                results["checked"] += 1

            elif status == "failed":
                results["failed"] += 1
                results["checked"] += 1

            elif status == "invalid":
                results["invalid"] += 1
                results["checked"] += 1

    return results
