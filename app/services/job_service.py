from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.job_repo import JobRepository
from app.schemas.job import JobCreate, JobRead


class JobService:
    def __init__(self, db: Session):
        self.repo = JobRepository(db)

    def list_jobs(self) -> list[JobRead]:
        return [JobRead.model_validate(job) for job in self.repo.list()]

    def create_job(self, payload: JobCreate) -> JobRead:
        job = Job(title=payload.title, description=payload.description, owner_id=payload.owner_id)
        created = self.repo.create(job)
        return JobRead.model_validate(created)
