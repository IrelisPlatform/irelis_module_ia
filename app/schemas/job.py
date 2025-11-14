from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str | None = None


class JobCreate(JobBase):
    owner_id: int


class JobRead(JobBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
