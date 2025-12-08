"""API routers for version 1."""

from . import (
    candidate_router,
    matching_router,
    offer_router,
    recruiter_router,
    search_router,
    sourcing_router,
)

__all__ = [
    "candidate_router",
    "matching_router",
    "recruiter_router",
    "offer_router",
    "search_router",
    "sourcing_router",
]
