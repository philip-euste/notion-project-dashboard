
import hmac
import time

import httpx

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.database.models import Project
from app.services.github_client import refresh_github_projects
from app.services.notion_client import update_notion_github_last_updated
from app.services.notion_sync import sync_notion_projects


router = APIRouter(prefix="/api/sync", tags=["Synchronization"])


def verify_sync_token(x_sync_token: str | None) -> None:
    if not settings.sync_secret:
        raise HTTPException(
            status_code=503,
            detail="Synchronization is not configured.",
        )

    if not x_sync_token or not hmac.compare_digest(
        x_sync_token,
        settings.sync_secret,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid synchronization token.",
        )


@router.post("/notion")
def sync_notion(
    x_sync_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    verify_sync_token(x_sync_token)

    try:
        result = sync_notion_projects(db)

        return {
            "message": "Notion synchronization completed.",
            **result,
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="Could not communicate with the Notion API.",
        ) from error


@router.post("/github")
def sync_github(
    x_sync_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    verify_sync_token(x_sync_token)

    try:
        statement = select(Project).order_by(Project.created_at.desc())
        projects = db.scalars(statement).all()

        result = refresh_github_projects(projects)

        db.commit()

        notion_results = {
            "notion_updated": 0,
            "notion_failed": 0,
            "notion_skipped": 0,
        }

        with httpx.Client(timeout=30.0) as client:
            for project in projects:
                if not project.notion_page_id or not project.github_pushed_at:
                    notion_results["notion_skipped"] += 1
                    continue

                try:
                    update_notion_github_last_updated(
                        project.notion_page_id,
                        project.github_pushed_at,
                        client,
                    )

                    notion_results["notion_updated"] += 1

                except (httpx.HTTPError, ValueError):
                    notion_results["notion_failed"] += 1

                time.sleep(0.35)

        return {
            "message": "GitHub synchronization completed.",
            **result,
            **notion_results,
        }

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="GitHub synchronization failed.",
        ) from error
