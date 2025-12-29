from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import ChatbotChannel, ChatbotSessionState


class ChatbotSendRequest(BaseModel):
    user_id: UUID
    content: str = Field(min_length=1)
    channel: ChatbotChannel
    lang: str | None = None
    session_id: UUID | None = None
    token: str | None = None
    threshold: float | None = Field(default=None, ge=0.0, le=1.0)


class ChatbotSessionInit(BaseModel):
    user_id: UUID
    channel: ChatbotChannel
    metadata_: dict | None = None
    force_new: bool = False


class ChatbotSessionClose(BaseModel):
    user_id: UUID
    session_id: UUID


class ChatbotSendResponse(BaseModel):
    session_id: UUID
    request_message_id: UUID
    response_message_id: UUID
    response: str
    faq_entry_id: UUID | None = None
    confidence: float | None = None
    handoff: bool
    state: ChatbotSessionState
    channel: ChatbotChannel
    created_at: datetime


class ChatbotFeedbackCreate(BaseModel):
    user_id: UUID
    session_id: UUID
    response_message_id: UUID
    rating: int = Field(ge=-1, le=1)
    comment: str | None = None


class ChatbotMessagesQuery(BaseModel):
    session_id: UUID | None = None
    channel: ChatbotChannel | None = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
