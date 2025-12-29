from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1 import deps
from app.models.enums import ChatbotChannel
from app.schemas import (
    ChatbotFeedbackCreate,
    ChatbotFeedbackRead,
    ChatbotMessageRead,
    ChatbotSendRequest,
    ChatbotSendResponse,
    ChatbotSessionClose,
    ChatbotSessionInit,
    ChatbotSessionRead,
)
from app.services.chatbot_service import ChatbotService


router = APIRouter()


@router.post(
    "/chat/send_request",
    response_model=ChatbotSendResponse,
    tags=["chatbot"],
)
def send_request(
    payload: ChatbotSendRequest,
    db: Annotated[Session, Depends(deps.get_db)],
) -> ChatbotSendResponse:
    """Create a request/response pair in a chatbot session."""
    service = ChatbotService(db)
    try:
        return service.send_request(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/chat/session/init",
    response_model=ChatbotSessionRead,
    tags=["chatbot"],
)
def init_session(
    payload: ChatbotSessionInit,
    db: Annotated[Session, Depends(deps.get_db)],
) -> ChatbotSessionRead:
    """Create or return the current session for a user/channel."""
    service = ChatbotService(db)
    return service.init_session(payload)


@router.post(
    "/chat/session/close",
    response_model=ChatbotSessionRead,
    tags=["chatbot"],
)
def close_session(
    payload: ChatbotSessionClose,
    db: Annotated[Session, Depends(deps.get_db)],
) -> ChatbotSessionRead:
    """Close a chatbot session for a user."""
    service = ChatbotService(db)
    try:
        return service.close_session(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/chat/session/current",
    response_model=ChatbotSessionRead,
    tags=["chatbot"],
)
def get_current_session(
    db: Annotated[Session, Depends(deps.get_db)],
    user_id: UUID = Query(...),
    channel: ChatbotChannel = Query(...),
) -> ChatbotSessionRead:
    """Return the current session for a user/channel."""
    service = ChatbotService(db)
    session = service.get_current_session(user_id, channel)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session introuvable.",
        )
    return session


@router.get(
    "/chat/user/{user_id}",
    response_model=list[ChatbotMessageRead],
    tags=["chatbot"],
)
def list_user_messages(
    user_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
    session_id: UUID | None = Query(default=None),
    channel: ChatbotChannel | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ChatbotMessageRead]:
    """Return paginated chatbot messages for a user."""
    service = ChatbotService(db)
    return service.list_messages(user_id, session_id, channel, limit, offset)


@router.get(
    "/chat/session/{session_id}/messages",
    response_model=list[ChatbotMessageRead],
    tags=["chatbot"],
)
def list_session_messages(
    session_id: UUID,
    db: Annotated[Session, Depends(deps.get_db)],
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ChatbotMessageRead]:
    """Return paginated messages for a specific session."""
    service = ChatbotService(db)
    return service.list_messages_for_session(session_id, limit, offset)


@router.post(
    "/chat/feedback",
    response_model=ChatbotFeedbackRead,
    tags=["chatbot"],
)
def create_feedback(
    payload: ChatbotFeedbackCreate,
    db: Annotated[Session, Depends(deps.get_db)],
) -> ChatbotFeedbackRead:
    """Store user feedback for a chatbot response."""
    service = ChatbotService(db)
    try:
        return service.create_feedback(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
