from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import (
    candidate_router,
    matching_router,
    offer_router,
    recruiter_router,
    search_router,
)
from app.db.init_db import init_db
from app.db.session import SessionLocal

app = FastAPI(title="IRELIS Module IA", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_router.router, prefix="/api/v1/candidats")
app.include_router(recruiter_router.router, prefix="/api/v1")
app.include_router(offer_router.router, prefix="/api/v1")
app.include_router(search_router.router, prefix="/api/v1")
app.include_router(matching_router.router, prefix="/api/v1")


@app.on_event("startup")
def startup_event() -> None:
    """
    Ensure database tables exist (creates missing ones) when the app boots.
    """
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


@app.get("/health", tags=["health"])  # lightweight uptime probe
async def health_check() -> dict[str, str]:
    return {"status": "Module IA is healthy, thanks for asking!"}
