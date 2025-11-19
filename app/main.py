from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import candidats
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

app.include_router(candidats.router, prefix="/api/v1/candidats", tags=["candidats"])


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
    return {"status": "ok"}
