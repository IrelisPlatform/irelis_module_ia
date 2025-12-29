from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import (
    ChatbotFaqEntry,
    ChatbotFeedback,
    ChatbotMessage,
    ChatbotSession,
    ChatbotUnmatchedQuestion,
)
from app.models.enums import ChatbotMessageType, ChatbotSessionState


class ChatbotRepository:
    """Persistence helpers for chatbot sessions and messages."""

    def __init__(self, db: Session):
        self.db = db

    def get_session(self, session_id: UUID) -> ChatbotSession | None:
        return self.db.query(ChatbotSession).filter_by(id=session_id).first()

    def get_current_session(
        self, user_id: UUID, channel: str
    ) -> ChatbotSession | None:
        return (
            self.db.query(ChatbotSession)
            .filter_by(
                user_id=user_id,
                channel=channel,
                state=ChatbotSessionState.CURRENT,
            )
            .first()
        )

    def create_session(
        self, user_id: UUID, channel: str, metadata: dict | None = None
    ) -> ChatbotSession:
        session = ChatbotSession(
            user_id=user_id,
            channel=channel,
            state=ChatbotSessionState.CURRENT,
            metadata_=metadata,
            last_activity_at=datetime.now(timezone.utc),
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update_session_activity(self, session: ChatbotSession) -> None:
        session.last_activity_at = datetime.now(timezone.utc)
        self.db.add(session)
        self.db.commit()

    def close_session(self, session: ChatbotSession) -> None:
        session.state = ChatbotSessionState.CLOSED
        session.ended_at = datetime.now(timezone.utc)
        self.db.add(session)
        self.db.commit()

    def create_message(
        self,
        session_id: UUID,
        user_id: UUID,
        content: str,
        message_type: ChatbotMessageType,
        channel: str,
        lang: str | None = None,
        token: str | None = None,
        faq_entry_id: UUID | None = None,
        confidence: float | None = None,
        handoff: bool = False,
    ) -> ChatbotMessage:
        message = ChatbotMessage(
            session_id=session_id,
            user_id=user_id,
            content=content,
            type=message_type,
            channel=channel,
            lang=lang,
            token=token,
            faq_entry_id=faq_entry_id,
            confidence=confidence,
            handoff=handoff,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def list_messages(
        self,
        user_id: UUID,
        session_id: UUID | None,
        limit: int,
        offset: int,
    ) -> list[ChatbotMessage]:
        query = (
            self.db.query(ChatbotMessage)
            .filter(ChatbotMessage.user_id == user_id)
            .order_by(ChatbotMessage.created_at.asc())
        )
        if session_id is not None:
            query = query.filter(ChatbotMessage.session_id == session_id)
        return query.limit(limit).offset(offset).all()

    def list_messages_by_session(
        self,
        session_id: UUID,
        limit: int,
        offset: int,
    ) -> list[ChatbotMessage]:
        return (
            self.db.query(ChatbotMessage)
            .filter(ChatbotMessage.session_id == session_id)
            .order_by(ChatbotMessage.created_at.asc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def list_active_faq_entries(
        self, lang: str | None = None
    ) -> list[ChatbotFaqEntry]:
        query = self.db.query(ChatbotFaqEntry).filter_by(is_active=True)
        if lang:
            query = query.filter(ChatbotFaqEntry.lang == lang)
        return query.all()

    def create_unmatched_question(
        self,
        user_id: UUID,
        session_id: UUID,
        request_message_id: UUID,
        content: str,
        lang: str | None,
        channel: str,
        reason: str,
        top_candidates: list[dict] | None,
    ) -> ChatbotUnmatchedQuestion:
        entry = ChatbotUnmatchedQuestion(
            user_id=user_id,
            session_id=session_id,
            request_message_id=request_message_id,
            content=content,
            lang=lang,
            channel=channel,
            reason=reason,
            top_candidates=top_candidates,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_message(self, message_id: UUID) -> ChatbotMessage | None:
        return self.db.query(ChatbotMessage).filter_by(id=message_id).first()

    def get_feedback_by_response(
        self, response_message_id: UUID
    ) -> ChatbotFeedback | None:
        return (
            self.db.query(ChatbotFeedback)
            .filter_by(response_message_id=response_message_id)
            .first()
        )

    def create_feedback(
        self,
        user_id: UUID,
        session_id: UUID,
        response_message_id: UUID,
        faq_entry_id: UUID | None,
        rating: int,
        comment: str | None,
    ) -> ChatbotFeedback:
        feedback = ChatbotFeedback(
            user_id=user_id,
            session_id=session_id,
            response_message_id=response_message_id,
            faq_entry_id=faq_entry_id,
            rating=rating,
            comment=comment,
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
