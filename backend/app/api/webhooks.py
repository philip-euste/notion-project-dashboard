
import hashlib
import hmac
import json
import logging

import httpx

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.database.models import Project
from app.services.notion_sync import sync_notion_projects


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/webhooks",
    tags=["Webhooks"],
)


SYNC_EVENTS = {
    "page.created",
    "page.properties_updated",
    "page.content_updated",
    "page.moved",
    "page.undeleted",
    "data_source.content_updated",
    "database.content_updated",
}


@router.post("/notion")
async def notion_webhook(
    request: Request,
    x_notion_signature: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    raw_body = await request.body()

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload.",
        ) from error

    # Initial subscription verification request.
    verification_token = payload.get("verification_token")

    if verification_token:
        logger.warning(
            "NOTION_WEBHOOK_VERIFICATION_TOKEN=%s",
            verification_token,
        )

        return {
            "message": "Verification token received."
        }

    # Verify all subsequent webhook requests.
    secret = settings.notion_webhook_secret

    if not secret:
        raise HTTPException(
            status_code=503,
            detail="Notion webhook secret is not configured.",
        )

    if not x_notion_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing Notion signature.",
        )

    calculated_signature = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(
        calculated_signature,
        x_notion_signature,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Notion signature.",
        )

    event_type = payload.get("type")
    entity = payload.get("entity") or {}
    entity_id = entity.get("id")

    # Handle page deletion directly.
    # This also works when the deleted page was the last project.
    if event_type == "page.deleted":
        if not entity_id:
            raise HTTPException(
                status_code=400,
                detail="Missing page ID.",
            )

        project = db.scalar(
            select(Project).where(
                Project.notion_page_id == entity_id
            )
        )

        if project is not None:
            db.delete(project)
            db.commit()

        return {
            "message": "Page deletion processed.",
            "deleted": project is not None,
        }

    # Ignore events that do not affect project data.
    if event_type not in SYNC_EVENTS:
        return {
            "message": "Event ignored.",
            "event_type": event_type,
        }

    try:
        result = sync_notion_projects(db)

        return {
            "message": "Notion webhook synchronization completed.",
            "event_type": event_type,
            **result,
        }

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="Could not communicate with the Notion API.",
        ) from error
