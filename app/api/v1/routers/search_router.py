from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.schemas import SearchRead
from app.services.search_service import SearchService

router = APIRouter()


@router.get("/searches", response_model=list[SearchRead], tags=["searches"])
def list_searches(db: Annotated[Session, Depends(deps.get_db)]) -> list[SearchRead]:
    return SearchService(db).list_searches()


@router.get("/searches/{search_id}", response_model=SearchRead, tags=["searches"])
def get_search(
    search_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> SearchRead:
    search = SearchService(db).get_search(search_id)
    if search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Search not found")
    return search


@router.get(
    "/users/{user_id}/searches",
    response_model=list[SearchRead],
    tags=["searches"],
)
def list_searches_by_user(
    user_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
) -> list[SearchRead]:
    return SearchService(db).list_by_user(user_id)
