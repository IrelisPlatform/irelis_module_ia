"""API routers for version 1."""

from . import (
    candidate_router,
    offer_router,
    offer_template_router,
    recruiter_router,
    search_router,
)

__all__ = [
    "candidate_router",
    "recruiter_router",
    "search_router",
    "offer_template_router",
    "offer_router",
]
