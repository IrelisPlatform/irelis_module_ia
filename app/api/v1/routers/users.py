from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=list[UserRead])
def list_users(db: Annotated[Session, Depends(deps.get_db)]) -> list[UserRead]:
    service = UserService(db)
    return service.list_users()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Annotated[Session, Depends(deps.get_db)],
) -> UserRead:
    service = UserService(db)
    try:
        return service.create_user(payload)
    except ValueError as exc:  # simple duplicate guard
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
