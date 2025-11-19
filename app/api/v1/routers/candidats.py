from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1 import deps

router = APIRouter()

@router.get("/health", tags=["health"])  # lightweight uptime probe
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
