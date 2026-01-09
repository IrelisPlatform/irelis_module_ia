from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.v1 import deps
from app.app import app
from app.models.enums import (
    ChatbotChannel,
    ChatbotMessageType,
    ChatbotSessionState,
)
from app.schemas import (
    ChatbotFeedbackRead,
    ChatbotMessageRead,
    ChatbotSendResponse,
    ChatbotSessionRead,
)


@pytest.fixture(autouse=True)
def _override_db_dependency():
    def _get_db():
        yield None

    app.dependency_overrides[deps.get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def _stub_chatbot_service(monkeypatch: pytest.MonkeyPatch):
    class StubChatbotService:
        def __init__(self, db):
            self.db = db

        def send_request(self, payload):
            return _sample_send_response()

        def init_session(self, payload):
            return _sample_session()

        def close_session(self, payload):
            return _sample_session()

        def get_current_session(self, user_id, channel):
            return _sample_session()

        def list_messages(self, user_id, session_id, channel, limit, offset):
            return _sample_messages()

        def list_messages_for_session(self, session_id, limit, offset):
            return _sample_messages()

        def create_feedback(self, payload):
            return _sample_feedback()

    monkeypatch.setattr(
        "app.api.v1.routers.chatbot_router.ChatbotService", StubChatbotService
    )


def _sample_session() -> ChatbotSessionRead:
    return ChatbotSessionRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        user_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        state=ChatbotSessionState.CURRENT,
        channel=ChatbotChannel.WEB,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ended_at=None,
        last_activity_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        metadata_={"user_agent": "pytest"},
    )


def _sample_send_response() -> ChatbotSendResponse:
    return ChatbotSendResponse(
        session_id=UUID("11111111-1111-1111-1111-111111111111"),
        request_message_id=UUID("22222222-2222-2222-2222-222222222222"),
        response_message_id=UUID("33333333-3333-3333-3333-333333333333"),
        response="Voici une reponse officielle.",
        faq_entry_id=UUID("44444444-4444-4444-4444-444444444444"),
        confidence=0.82,
        handoff=False,
        state=ChatbotSessionState.CURRENT,
        channel=ChatbotChannel.WEB,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )


def _sample_messages() -> list[ChatbotMessageRead]:
    return [
        ChatbotMessageRead(
            id=UUID("55555555-5555-5555-5555-555555555555"),
            session_id=UUID("11111111-1111-1111-1111-111111111111"),
            user_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            content="Bonjour",
            type=ChatbotMessageType.REQUEST,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            channel=ChatbotChannel.WEB,
            lang="fr",
            token=None,
            faq_entry_id=None,
            confidence=None,
            handoff=False,
        ),
        ChatbotMessageRead(
            id=UUID("66666666-6666-6666-6666-666666666666"),
            session_id=UUID("11111111-1111-1111-1111-111111111111"),
            user_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            content="Voici une reponse.",
            type=ChatbotMessageType.RESPONSE,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            channel=ChatbotChannel.WEB,
            lang="fr",
            token=None,
            faq_entry_id=UUID("44444444-4444-4444-4444-444444444444"),
            confidence=0.8,
            handoff=False,
        ),
    ]


def _sample_feedback() -> ChatbotFeedbackRead:
    return ChatbotFeedbackRead(
        id=UUID("77777777-7777-7777-7777-777777777777"),
        user_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        session_id=UUID("11111111-1111-1111-1111-111111111111"),
        response_message_id=UUID("33333333-3333-3333-3333-333333333333"),
        faq_entry_id=UUID("44444444-4444-4444-4444-444444444444"),
        rating=1,
        comment="Merci !",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )


def test_chat_send_request() -> None:
    client = TestClient(app)
    payload = {
        "user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "content": "Bonjour",
        "channel": "web",
    }
    response = client.post("/api/v1/chat/send_request", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["response"] == "Voici une reponse officielle."
    assert body["handoff"] is False


def test_chat_session_init() -> None:
    client = TestClient(app)
    payload = {
        "user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "channel": "web",
        "metadata_": {"user_agent": "pytest"},
        "force_new": True,
    }
    response = client.post("/api/v1/chat/session/init", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "current"
    assert body["channel"] == "web"


def test_chat_session_close() -> None:
    client = TestClient(app)
    payload = {
        "user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "session_id": "11111111-1111-1111-1111-111111111111",
    }
    response = client.post("/api/v1/chat/session/close", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "11111111-1111-1111-1111-111111111111"


def test_chat_session_current() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/chat/session/current",
        params={"user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "channel": "web"},
    )
    assert response.status_code == 200
    assert response.json()["state"] == "current"


def test_chat_user_messages() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/chat/user/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        params={"limit": 10, "offset": 0},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["type"] == "request"


def test_chat_session_messages() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/chat/session/11111111-1111-1111-1111-111111111111/messages",
        params={"limit": 10, "offset": 0},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[1]["type"] == "response"


def test_chat_feedback() -> None:
    client = TestClient(app)
    payload = {
        "user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "session_id": "11111111-1111-1111-1111-111111111111",
        "response_message_id": "33333333-3333-3333-3333-333333333333",
        "rating": 1,
        "comment": "Merci !",
    }
    response = client.post("/api/v1/chat/feedback", json=payload)
    assert response.status_code == 200
    assert response.json()["rating"] == 1
