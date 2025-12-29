from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from datetime import datetime, timezone
from typing import Iterable
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import (
    ChatbotChannel,
    ChatbotMessageType,
    ChatbotSessionState,
    ChatbotUnmatchedReason,
)
from app.repositories.chatbot_repository import ChatbotRepository
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


@dataclass
class _CandidateScore:
    faq_id: UUID
    score: float


class ChatbotService:
    """Business logic for the FAQ-only chatbot."""

    def __init__(self, db: Session, default_threshold: float = 0.6):
        self.repo = ChatbotRepository(db)
        self.default_threshold = default_threshold

    def send_request(self, payload: ChatbotSendRequest) -> ChatbotSendResponse:
        session = None
        if payload.session_id:
            session = self.repo.get_session(payload.session_id)

        if session is None:
            session = self.repo.get_current_session(payload.user_id, payload.channel)

        if session is None:
            session = self.repo.create_session(
                payload.user_id,
                payload.channel,
                metadata=None,
            )
        else:
            if session.user_id != payload.user_id:
                raise ValueError("Session utilisateur invalide.")
            if session.channel != payload.channel:
                raise ValueError("Canal invalide pour la session.")

        request_message = self.repo.create_message(
            session_id=session.id,
            user_id=payload.user_id,
            content=payload.content,
            message_type=ChatbotMessageType.REQUEST,
            channel=payload.channel,
            lang=payload.lang,
            token=payload.token,
        )
        self.repo.update_session_activity(session)

        threshold = (
            payload.threshold
            if payload.threshold is not None
            else self.default_threshold
        )
        candidates, faq_map = self._score_faq_entries(payload.content, payload.lang)
        best = candidates[0] if candidates else None

        response_text = self._fallback_message(payload.lang)
        faq_entry_id = None
        confidence = None
        handoff = True

        if best and best.score >= threshold:
            matched_entry = faq_map.get(best.faq_id)
            if matched_entry:
                response_text = matched_entry.answer
                faq_entry_id = matched_entry.id
                confidence = best.score
                handoff = False

        response_message = self.repo.create_message(
            session_id=session.id,
            user_id=payload.user_id,
            content=response_text,
            message_type=ChatbotMessageType.RESPONSE,
            channel=payload.channel,
            lang=payload.lang,
            faq_entry_id=faq_entry_id,
            confidence=confidence,
            handoff=handoff,
        )
        self.repo.update_session_activity(session)

        if handoff:
            top_candidates = [
                {"faq_entry_id": str(candidate.faq_id), "score": candidate.score}
                for candidate in candidates[:3]
            ]
            reason = (
                ChatbotUnmatchedReason.LOW_CONFIDENCE
                if top_candidates
                else ChatbotUnmatchedReason.NO_MATCH
            )
            self.repo.create_unmatched_question(
                user_id=payload.user_id,
                session_id=session.id,
                request_message_id=request_message.id,
                content=payload.content,
                lang=payload.lang,
                channel=payload.channel,
                reason=reason,
                top_candidates=top_candidates or None,
            )

        return ChatbotSendResponse(
            session_id=session.id,
            request_message_id=request_message.id,
            response_message_id=response_message.id,
            response=response_text,
            faq_entry_id=faq_entry_id,
            confidence=confidence,
            handoff=handoff,
            state=ChatbotSessionState.CURRENT,
            channel=payload.channel,
            created_at=response_message.created_at
            if isinstance(response_message.created_at, datetime)
            else datetime.now(timezone.utc),
        )

    def init_session(self, payload: ChatbotSessionInit) -> ChatbotSessionRead:
        session = self.repo.get_current_session(payload.user_id, payload.channel)
        if session is not None and payload.force_new:
            self.repo.close_session(session)
            session = None
        if session is None:
            session = self.repo.create_session(
                payload.user_id, payload.channel, payload.metadata_
            )
        return ChatbotSessionRead.model_validate(session)

    def close_session(self, payload: ChatbotSessionClose) -> ChatbotSessionRead:
        session = self.repo.get_session(payload.session_id)
        if session is None:
            raise ValueError("Session introuvable.")
        if session.user_id != payload.user_id:
            raise ValueError("Session utilisateur invalide.")
        if session.state == ChatbotSessionState.CLOSED:
            return ChatbotSessionRead.model_validate(session)
        self.repo.close_session(session)
        return ChatbotSessionRead.model_validate(session)

    def get_current_session(
        self, user_id: UUID, channel: ChatbotChannel
    ) -> ChatbotSessionRead | None:
        session = self.repo.get_current_session(user_id, channel)
        if session is None:
            return None
        return ChatbotSessionRead.model_validate(session)

    def list_messages(
        self,
        user_id: UUID,
        session_id: UUID | None,
        channel: ChatbotChannel | None,
        limit: int,
        offset: int,
    ) -> list[ChatbotMessageRead]:
        if session_id is None and channel is not None:
            session = self.repo.get_current_session(user_id, channel)
            session_id = session.id if session else None
        messages = self.repo.list_messages(user_id, session_id, limit, offset)
        return [ChatbotMessageRead.model_validate(message) for message in messages]

    def list_messages_for_session(
        self, session_id: UUID, limit: int, offset: int
    ) -> list[ChatbotMessageRead]:
        messages = self.repo.list_messages_by_session(session_id, limit, offset)
        return [ChatbotMessageRead.model_validate(message) for message in messages]

    def create_feedback(
        self, payload: ChatbotFeedbackCreate
    ) -> ChatbotFeedbackRead:
        existing = self.repo.get_feedback_by_response(payload.response_message_id)
        if existing:
            raise ValueError("Feedback deja enregistre pour ce message.")

        message = self.repo.get_message(payload.response_message_id)
        if message is None or message.type != ChatbotMessageType.RESPONSE:
            raise ValueError("Message de reponse introuvable.")

        feedback = self.repo.create_feedback(
            user_id=payload.user_id,
            session_id=payload.session_id,
            response_message_id=payload.response_message_id,
            faq_entry_id=message.faq_entry_id,
            rating=payload.rating,
            comment=payload.comment,
        )
        return ChatbotFeedbackRead.model_validate(feedback)

    def _score_faq_entries(
        self, request_text: str, lang: str | None
    ) -> tuple[list[_CandidateScore], dict[UUID, object]]:
        entries = self.repo.list_active_faq_entries(lang)
        scores: list[_CandidateScore] = []
        for entry in entries:
            score = self._compute_similarity(
                request_text, entry.question, entry.keywords or []
            )
            scores.append(_CandidateScore(entry.id, score))
        scores.sort(key=lambda item: item.score, reverse=True)
        return scores, {entry.id: entry for entry in entries}

    def _compute_similarity(
        self, request_text: str, question: str, keywords: Iterable[str]
    ) -> float:
        request_tokens = self._tokenize(request_text)
        question_tokens = self._tokenize(question)
        keyword_tokens = {token.lower() for token in keywords if token}

        jaccard = self._jaccard(request_tokens, question_tokens)
        seq = SequenceMatcher(
            None, request_text.lower().strip(), question.lower().strip()
        ).ratio()
        keyword_bonus = 0.0
        if keyword_tokens:
            hits = len(request_tokens & keyword_tokens)
            keyword_bonus = 0.1 * (hits / max(1, len(keyword_tokens)))
        return min(1.0, (0.6 * seq) + (0.4 * jaccard) + keyword_bonus)

    def _tokenize(self, text: str) -> set[str]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        return set(tokens)

    def _jaccard(self, left: set[str], right: set[str]) -> float:
        if not left and not right:
            return 0.0
        intersection = left & right
        union = left | right
        return len(intersection) / max(1, len(union))

    def _fallback_message(self, lang: str | None) -> str:
        if lang == "en":
            return (
                "I am not sure about the answer. Please contact support "
                "via WhatsApp or Telegram for assistance."
            )
        return (
            "Je ne suis pas certain de la reponse. "
            "Merci de contacter le support via WhatsApp ou Telegram."
        )
