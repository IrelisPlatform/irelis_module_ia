from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.v1 import deps
from app.app import app
from app.schemas import (
    CandidateRead,
    CandidateRecommendationsResponse,
    CandidateMatch,
    JobOfferMatch,
    JobOfferRead,
    MatchingScoreResponse,
    SourcingSearchResponse,
)


@pytest.fixture(autouse=True)
def _override_db_dependency():
    def _get_db():
        yield None

    app.dependency_overrides[deps.get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def _stub_services(monkeypatch: pytest.MonkeyPatch):
    class StubCandidateService:
        def __init__(self, db):
            self.db = db

        def list_candidates(self):
            return [_sample_candidate()]

        def search_by_boolean_query(self, query, user_id):
            return [_sample_candidate()]

    class StubSearchService:
        def __init__(self, db):
            self.db = db

        def search_by_payload(self, payload):
            return [_sample_offer()]

        def search_for_candidate_by_user(self, user_id, payload=None):
            return [_sample_offer()]

    class StubMatchingService:
        def __init__(self, db):
            self.db = db

        def score_candidate_for_offer(self, candidate_id, offer_id):
            return MatchingScoreResponse(score=0.75, matched_skills=["python"])

        def recommend_offers_for_candidate(self, candidate_id, k):
            return _sample_recommendations()

        def rank_candidates_for_offer(self, offer_id, limit):
            return _sample_sourcing()

    monkeypatch.setattr(
        "app.api.v1.routers.candidate_router.CandidateService",
        StubCandidateService,
    )
    monkeypatch.setattr(
        "app.api.v1.routers.search_router.SearchService",
        StubSearchService,
    )
    monkeypatch.setattr(
        "app.api.v1.routers.matching_router.MatchingService",
        StubMatchingService,
    )
    monkeypatch.setattr(
        "app.api.v1.routers.sourcing_router.MatchingService",
        StubMatchingService,
    )


def _sample_candidate() -> CandidateRead:
    return CandidateRead(
        id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        user_id=UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
    )


def _sample_offer() -> JobOfferRead:
    return JobOfferRead(
        id=UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),
        company_id=UUID("dddddddd-dddd-dddd-dddd-dddddddddddd"),
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=None,
    )


def _sample_recommendations() -> CandidateRecommendationsResponse:
    offer_match = JobOfferMatch(
        offer=_sample_offer(),
        score=0.8,
        matched_skills=["python"],
    )
    return CandidateRecommendationsResponse(offers=[offer_match])


def _sample_sourcing() -> SourcingSearchResponse:
    candidate = CandidateMatch(
        id=UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"),
        name="Test Candidate",
        score=0.9,
        location="Paris",
        skills=["python"],
    )
    return SourcingSearchResponse(candidates=[candidate])


def test_list_candidates() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/candidats")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


def test_boolean_search_candidates() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/candidats/recherche/bool",
        params={
            "user_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "query": "python AND data",
        },
    )
    assert response.status_code == 200
    assert response.json()[0]["id"] == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


def test_search_offers_without_user() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/recherches/offres")
    assert response.status_code == 200
    assert response.json()["content"][0]["id"] == "cccccccc-cccc-cccc-cccc-cccccccccccc"


def test_search_offers_with_user() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/recherches/offres",
        params={"user_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"},
    )
    assert response.status_code == 200
    assert response.json()["content"][0]["id"] == "cccccccc-cccc-cccc-cccc-cccccccccccc"


def test_matching_score() -> None:
    client = TestClient(app)
    payload = {
        "candidate_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "offer_id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
    }
    response = client.post("/api/v1/matching/score", json=payload)
    assert response.status_code == 200
    assert response.json()["score"] == 0.75


def test_recommendations() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/recommendations",
        params={"candidateId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "k": 5},
    )
    assert response.status_code == 200
    assert response.json()["offers"][0]["score"] == 0.8


def test_sourcing_search() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/sourcing/search",
        params={"offerId": "cccccccc-cccc-cccc-cccc-cccccccccccc", "limit": 5},
    )
    assert response.status_code == 200
    assert response.json()["candidates"][0]["name"] == "Test Candidate"
