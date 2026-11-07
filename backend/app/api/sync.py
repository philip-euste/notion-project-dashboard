
import hmac

import httpx

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.services.notion_sync import sync_notion_projects


router = APIRouter(prefix="/api/sync", tags=["Synchronization"])


@router.post("/notion")
def sync_notion(
    x_sync_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
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
