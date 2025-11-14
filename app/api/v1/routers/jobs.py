from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas.job import JobCreate, JobRead
from app.services.job_service import JobService

router = APIRouter()


@router.get("/", response_model=list[JobRead])
def list_jobs(db: Annotated[Session, Depends(deps.get_db)]) -> list[JobRead]:
    return JobService(db).list_jobs()


@router.post("/", response_model=JobRead)
def create_job(
    payload: JobCreate,
    db: Annotated[Session, Depends(deps.get_db)],
) -> JobRead:
    return JobService(db).create_job(payload)
