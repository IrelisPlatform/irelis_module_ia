from __future__ import annotations

from typing import Annotated
from uuid import UUID
import os

from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from sqlalchemy.orm import Session

from pypdf import PdfReader

from app.api.v1 import deps
from app.schemas import (
    CandidateRecommendationsResponse,
    MatchingScoreRequest,
    MatchingScoreResponse,
)
from app.services.matching_service import MatchingService
from app.utils.cache import APP_CACHE, make_cache_key


router = APIRouter()

OUTPUT_DIR = "./"


@router.post(
    "/matching/score",
    # response_model=MatchingScoreResponse,
    tags=["matching"],
)
def compute_matching_score(
    payload: MatchingScoreRequest,
    db: Annotated[Session, Depends(deps.get_db)],
):
    #-> MatchingScoreResponse
    """Compute a compatibility score between one job offer and one candidate using his profile in the database."""
    service = MatchingService(db)
    result = service.score_candidate_for_offer(payload.candidate_id, payload.offer_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidat ou offre introuvable",
        )
    return result

@router.post(
    '/matching/cv/job_offer/{job_offer_id}',
    # response_model=MatchingScoreResponse,
    tags=['matching']
)
async def compute_matching_score_cv(
    db: Annotated[Session, Depends(deps.get_db)],
    job_offer_id: UUID,
    file: UploadFile = File(...)
):
    """Return the matchig percentage between a cv and a job offer."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    try:
        reader = PdfReader(file.file)
        full_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        if len(full_text) == 0:
            raise HTTPException(status_code=500, detail="Failed to read content of the pdf")
        full_text = [ line.replace(' ', '')for line in full_text]
        final_content =  "".join(full_text)

        service = MatchingService(db)
        response = service.matching_cv_job_offer(job_offer_id, final_content)
        
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer Not Found",
            )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
        
    finally:
        # Always close the uploaded file handle
        await file.close()


@router.get(
    "/recommendations",
    response_model=CandidateRecommendationsResponse,
    tags=["matching"],
)
def get_recommendations(
    db: Annotated[Session, Depends(deps.get_db)],
    candidate_id: UUID = Query(..., alias="candidateId"),
    k: int = Query(10, ge=1, le=50),
) -> CandidateRecommendationsResponse:
    """Return the top-k offers ranked for the provided candidate based on his profil."""

    service = MatchingService(db)
    response = service.recommend_offers_for_candidate(candidate_id, k)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate Not Found",
        )

    return response
