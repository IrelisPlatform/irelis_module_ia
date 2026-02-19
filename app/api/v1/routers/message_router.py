from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session

# À adapter selon l'arborescence exacte de ton projet
from app.api.v1 import deps
from app.schemas import (
    BlockCreate,
    BlockResponse,
    ConversationSummary,
    MessageCreate,
    MessageResponse,
)
from app.services.message_service import ChatService

router = APIRouter(prefix="/chat", tags=["Messagerie"])

@router.post("/send", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    db: Annotated[Session, Depends(deps.get_db)],
) -> MessageResponse:
    """Send a message to another user. Return 403 if the user is blocked."""
    return ChatService(db).send_message(message)


@router.get("/inbox", response_model=list[ConversationSummary])
def get_inbox(
    db: Annotated[Session, Depends(deps.get_db)],
    current_user_id: UUID,
) -> list[ConversationSummary]:
    """ Get the inbox of the current user."""
    return ChatService(db).get_inbox(current_user_id)


@router.get("/history", response_model=list[MessageResponse])
def get_chat_history(
    db: Annotated[Session, Depends(deps.get_db)],
    other_user_id: UUID,
    current_user_id: UUID,
) -> list[MessageResponse]:
    """Get messages between two users."""
    return ChatService(db).get_history(current_user_id, other_user_id)


# @router.post("/block", response_model=BlockResponse)
def block_unblock_user(
    block_data: BlockCreate,
    db: Annotated[Session, Depends(deps.get_db)],
    current_user_id: UUID,
) -> BlockResponse:
    """Block or unblock a user(Toggle)."""
    is_now_blocked = ChatService(db).toggle_block_user(current_user_id, block_data.user_id_to_block)
    status_msg = "User blocked" if is_now_blocked else "User unblocked"
    return BlockResponse(message=status_msg, is_blocked=is_now_blocked)