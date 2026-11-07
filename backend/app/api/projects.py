
from datetime import datetime, timezone
from uuid import UUID

import httpx

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    validate_status_pair,
)
from app.services.notion_client import (
    create_notion_page,
    update_notion_page,
    archive_notion_page,
)


router = APIRouter(prefix="/api/projects", tags=["Projects"])


def get_project_data(project: Project) -> dict:
    return {
        "name": project.name,
        "status_group": project.status_group,
        "status": project.status,
        "next_possible_action": project.next_possible_action,
        "potential": project.potential,
        "priority": project.priority,
        "repository": project.repository,
        "ide": project.ide,
        "skills": project.skills,
        "last_updated": project.last_updated,
    }


@router.get("/", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    statement = select(Project).order_by(Project.created_at.desc())
    return db.scalars(statement).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    project_values = project_data.model_dump()

    try:
        notion_page = create_notion_page(project_values)

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="Could not create the project in Notion.",
        ) from error

    project = Project(
        **project_values,
        notion_page_id=notion_page["id"],
        last_synced_at=datetime.now(timezone.utc),
    )

    try:
        db.add(project)
        db.commit()
        db.refresh(project)

    except Exception as error:
        db.rollback()

        try:
            archive_notion_page(notion_page["id"])
        except httpx.HTTPError:
            pass

        raise HTTPException(
            status_code=500,
            detail="Project creation failed in the database.",
        ) from error

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    updates = project_data.model_dump(exclude_unset=True)

    new_group = updates.get("status_group", project.status_group)
    new_status = updates.get("status", project.status)

    try:
        validate_status_pair(new_group, new_status)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    # Build the complete updated project without modifying the ORM object yet.
    project_values = get_project_data(project)
    project_values.update(updates)

    try:
        if project.notion_page_id:
            update_notion_page(
                project.notion_page_id,
                project_values,
            )
            notion_page_id = project.notion_page_id

        else:
            notion_page = create_notion_page(project_values)
            notion_page_id = notion_page["id"]

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="Could not update the project in Notion.",
        ) from error

    # Apply database changes after the Notion request succeeds.
    for field, value in updates.items():
        setattr(project, field, value)

    project.notion_page_id = notion_page_id
    project.last_synced_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(project)

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Notion was updated, but the database update failed. "
                   "A reconciliation may be required.",
        ) from error

    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.notion_page_id:
        try:
            archive_notion_page(project.notion_page_id)

        except httpx.HTTPError as error:
            raise HTTPException(
                status_code=502,
                detail="Could not archive the project in Notion.",
            ) from error

    try:
        db.delete(project)
        db.commit()

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Notion was archived, but database deletion failed. "
                   "A reconciliation may be required.",
        ) from error

    return Response(status_code=204)
