from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

import app.app as app_module
from app.api.v1 import deps
from app.services.candidate_service import CandidateService
from app.services.chatbot_service import ChatbotService
from app.services.matching_service import MatchingService
from app.services.search_service import SearchService


NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)


class DummySession:
    def close(self) -> None:
        return None


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    def override_get_db():
        yield DummySession()

    app_module.app.dependency_overrides[deps.get_db] = override_get_db
    monkeypatch.setattr(app_module, "SessionLocal", lambda: DummySession())
    monkeypatch.setattr(app_module, "init_db", lambda db: None)

    with TestClient(app_module.app) as test_client:
        yield test_client

    app_module.app.dependency_overrides.clear()


def job_offer_payload(offer_id=None) -> dict:
    return {"id": str(offer_id or uuid4()), "title": "Backend Engineer"}


def candidate_payload(candidate_id=None) -> dict:
    return {
        "id": str(candidate_id or uuid4()),
        "firstName": "Ada",
        "lastName": "Lovelace",
    }


def chatbot_session_payload(session_id=None, user_id=None) -> dict:
    return {
        "id": str(session_id or uuid4()),
        "user_id": str(user_id or uuid4()),
        "state": "current",
        "channel": "web",
        "created_at": NOW.isoformat(),
    }


def chatbot_message_payload(message_id=None, user_id=None, session_id=None) -> dict:
    return {
        "id": str(message_id or uuid4()),
        "session_id": str(session_id or uuid4()),
        "user_id": str(user_id or uuid4()),
        "content": "Hello",
        "type": "response",
        "created_at": NOW.isoformat(),
        "handoff": False,
        "channel": "web",
    }


def chatbot_feedback_payload(feedback_id=None, response_message_id=None) -> dict:
    return {
        "id": str(feedback_id or uuid4()),
        "response_message_id": str(response_message_id or uuid4()),
        "rating": 1,
        "created_at": NOW.isoformat(),
    }


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"].startswith("Module IA is healthy")


def test_list_candidates(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        CandidateService,
        "list_candidates",
        lambda self: [candidate_payload()],
    )
    response = client.get("/api/v1/candidats")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_boolean_search_candidates_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        CandidateService,
        "search_by_boolean_query",
        lambda self, query, user_id: [candidate_payload()],
    )
    response = client.get(
        "/api/v1/candidats/recherche/bool",
        params={"user_id": str(uuid4()), "query": "python AND fastapi"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_boolean_search_candidates_value_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_value_error(self, query, user_id):
        raise ValueError("Invalid query")

    monkeypatch.setattr(CandidateService, "search_by_boolean_query", raise_value_error)
    response = client.get(
        "/api/v1/candidats/recherche/bool",
        params={"user_id": str(uuid4()), "query": "BAD QUERY"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid query"


def test_boolean_search_candidates_lookup_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_lookup_error(self, query, user_id):
        raise LookupError("Utilisateur introuvable")

    monkeypatch.setattr(CandidateService, "search_by_boolean_query", raise_lookup_error)
    response = client.get(
        "/api/v1/candidats/recherche/bool",
        params={"user_id": str(uuid4()), "query": "python"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Utilisateur introuvable"


def test_boolean_search_candidates_permission_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_permission_error(self, query, user_id):
        raise PermissionError("No recruiter account")

    monkeypatch.setattr(
        CandidateService, "search_by_boolean_query", raise_permission_error
    )
    response = client.get(
        "/api/v1/candidats/recherche/bool",
        params={"user_id": str(uuid4()), "query": "python"},
    )
    assert response.status_code == 403


def test_search_offers_without_user_id(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    offers = [job_offer_payload(), job_offer_payload(), job_offer_payload()]
    monkeypatch.setattr(SearchService, "search_by_payload", lambda self, filters: offers)
    response = client.get("/api/v1/recherches/offres", params={"page": 0, "size": 2})
    data = response.json()
    assert response.status_code == 200
    assert data["total_elements"] == 3
    assert data["total_pages"] == 2
    assert data["first"] is True
    assert data["last"] is False
    assert len(data["content"]) == 2


def test_search_offers_with_user_not_found(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        SearchService,
        "search_for_candidate_by_user",
        lambda self, user_id, filters: None,
    )
    response = client.get(
        "/api/v1/recherches/offres",
        params={"user_id": str(uuid4())},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidat introuvable"


def test_recommend_offers_from_history_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        SearchService,
        "recommend_offers_from_search_history",
        lambda self, user_id, history_limit: [job_offer_payload()],
    )
    response = client.get(
        "/api/v1/recherches/offres/recommandations",
        params={"user_id": str(uuid4()), "history_limit": 3},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["total_elements"] == 1
    assert len(data["content"]) == 1


def test_recommend_offers_from_history_not_found(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        SearchService,
        "recommend_offers_from_search_history",
        lambda self, user_id, history_limit: None,
    )
    response = client.get(
        "/api/v1/recherches/offres/recommandations",
        params={"user_id": str(uuid4())},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Utilisateur introuvable"


def test_matching_score_ok(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        MatchingService,
        "score_candidate_for_offer",
        lambda self, candidate_id, offer_id: {
            "score": 0.92,
            "matched_skills": ["python"],
        },
    )
    payload = {"candidate_id": str(uuid4()), "offer_id": str(uuid4())}
    response = client.post("/api/v1/matching/score", json=payload)
    assert response.status_code == 200
    assert response.json()["score"] == 0.92


def test_matching_score_not_found(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        MatchingService,
        "score_candidate_for_offer",
        lambda self, candidate_id, offer_id: None,
    )
    payload = {"candidate_id": str(uuid4()), "offer_id": str(uuid4())}
    response = client.post("/api/v1/matching/score", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidat ou offre introuvable"


def test_matching_recommendations_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        MatchingService,
        "recommend_offers_for_candidate",
        lambda self, candidate_id, k: {
            "offers": [
                {
                    "offer": job_offer_payload(),
                    "score": 0.8,
                    "matched_skills": ["fastapi"],
                }
            ]
        },
    )
    response = client.get(
        "/api/v1/recommendations",
        params={"candidateId": str(uuid4()), "k": 5},
    )
    assert response.status_code == 200
    assert response.json()["offers"][0]["score"] == 0.8


def test_matching_recommendations_not_found(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        MatchingService,
        "recommend_offers_for_candidate",
        lambda self, candidate_id, k: None,
    )
    response = client.get(
        "/api/v1/recommendations",
        params={"candidateId": str(uuid4())},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidat introuvable"


def test_sourcing_search_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        MatchingService,
        "rank_candidates_for_offer",
        lambda self, offer_id, limit: {
            "candidates": [
                {"id": str(uuid4()), "name": "Alex", "score": 0.75}
            ]
        },
    )
    response = client.get(
        "/api/v1/sourcing/search",
        params={"offerId": str(uuid4()), "limit": 2},
    )
    assert response.status_code == 200
    assert response.json()["candidates"][0]["name"] == "Alex"


def test_sourcing_search_not_found(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        MatchingService,
        "rank_candidates_for_offer",
        lambda self, offer_id, limit: None,
    )
    response = client.get(
        "/api/v1/sourcing/search",
        params={"offerId": str(uuid4())},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Offre introuvable"


def test_chat_send_request_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "send_request",
        lambda self, payload: {
            "session_id": str(uuid4()),
            "request_message_id": str(uuid4()),
            "response_message_id": str(uuid4()),
            "response": "Hello",
            "faq_entry_id": None,
            "confidence": 0.9,
            "handoff": False,
            "state": "current",
            "channel": "web",
            "created_at": NOW,
        },
    )
    payload = {
        "user_id": str(uuid4()),
        "content": "Hi",
        "channel": "web",
    }
    response = client.post("/api/v1/chat/send_request", json=payload)
    assert response.status_code == 200
    assert response.json()["response"] == "Hello"


def test_chat_send_request_value_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_value_error(self, payload):
        raise ValueError("Session utilisateur invalide.")

    monkeypatch.setattr(ChatbotService, "send_request", raise_value_error)
    payload = {
        "user_id": str(uuid4()),
        "content": "Hi",
        "channel": "web",
    }
    response = client.post("/api/v1/chat/send_request", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Session utilisateur invalide."


def test_chat_init_session_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "init_session",
        lambda self, payload: chatbot_session_payload(),
    )
    payload = {"user_id": str(uuid4()), "channel": "web"}
    response = client.post("/api/v1/chat/session/init", json=payload)
    assert response.status_code == 200
    assert response.json()["state"] == "current"


def test_chat_close_session_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "close_session",
        lambda self, payload: chatbot_session_payload(
            session_id=payload.session_id, user_id=payload.user_id
        ),
    )
    payload = {"user_id": str(uuid4()), "session_id": str(uuid4())}
    response = client.post("/api/v1/chat/session/close", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == payload["session_id"]


def test_chat_close_session_value_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_value_error(self, payload):
        raise ValueError("Session introuvable.")

    monkeypatch.setattr(ChatbotService, "close_session", raise_value_error)
    payload = {"user_id": str(uuid4()), "session_id": str(uuid4())}
    response = client.post("/api/v1/chat/session/close", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Session introuvable."


def test_chat_get_current_session_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "get_current_session",
        lambda self, user_id, channel: chatbot_session_payload(user_id=user_id),
    )
    response = client.get(
        "/api/v1/chat/session/current",
        params={"user_id": str(uuid4()), "channel": "web"},
    )
    assert response.status_code == 200
    assert response.json()["channel"] == "web"


def test_chat_get_current_session_not_found(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService, "get_current_session", lambda self, user_id, channel: None
    )
    response = client.get(
        "/api/v1/chat/session/current",
        params={"user_id": str(uuid4()), "channel": "web"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Session introuvable."


def test_chat_list_user_messages_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "list_messages",
        lambda self, user_id, session_id, channel, limit, offset: [
            chatbot_message_payload(user_id=user_id, session_id=session_id)
        ],
    )
    user_id = str(uuid4())
    response = client.get(f"/api/v1/chat/user/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_chat_list_session_messages_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "list_messages_for_session",
        lambda self, session_id, limit, offset: [
            chatbot_message_payload(session_id=session_id)
        ],
    )
    session_id = str(uuid4())
    response = client.get(f"/api/v1/chat/session/{session_id}/messages")
    assert response.status_code == 200
    assert response.json()[0]["session_id"] == session_id


def test_chat_create_feedback_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ChatbotService,
        "create_feedback",
        lambda self, payload: chatbot_feedback_payload(
            response_message_id=payload.response_message_id
        ),
    )
    payload = {
        "user_id": str(uuid4()),
        "session_id": str(uuid4()),
        "response_message_id": str(uuid4()),
        "rating": 1,
    }
    response = client.post("/api/v1/chat/feedback", json=payload)
    assert response.status_code == 200
    assert response.json()["response_message_id"] == payload["response_message_id"]


def test_chat_create_feedback_value_error(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_value_error(self, payload):
        raise ValueError("Message de reponse introuvable.")

    monkeypatch.setattr(ChatbotService, "create_feedback", raise_value_error)
    payload = {
        "user_id": str(uuid4()),
        "session_id": str(uuid4()),
        "response_message_id": str(uuid4()),
        "rating": 1,
    }
    response = client.post("/api/v1/chat/feedback", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Message de reponse introuvable."
