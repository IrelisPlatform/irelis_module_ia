from __future__ import annotations

from typing import Annotated
from uuid import UUID
import os

from app.models.entities import JobOffer
from app.services.ai.ai_matchind_service import AIMatchingService
from app.services.ai.scraping_service import WebScrapingService
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
from google import genai


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
    '/matching/cv/job_offer',
    response_model=MatchingScoreResponse,
    tags=['matching']
)
async def compute_matching_score_cv(
    db: Annotated[Session, Depends(deps.get_db)],
    link: str = Query(...),
    file: UploadFile = File(...)
)-> MatchingScoreResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
        
    try:
        offer = None
        
        # --- LOGIQUE DE ROUTAGE (DB vs SCRAPING) ---
        if "irelis.net/jobs/" in link:
            job_offer_id = UUID(link[-36:])  
            offer = db.query(JobOffer).filter(JobOffer.id == job_offer_id).first()
            if not offer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internal Offer Not Found")
        else:
            scraper = WebScrapingService()
            
            offer = await scraper.scrape_and_extract_offer(link)
            if not offer:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                    detail="Impossible d'extraire l'offre d'emploi depuis ce lien externe."
                )

        # --- EXTRACTION DU CV ---
        reader = PdfReader(file.file)
        full_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        if not full_text:
            raise HTTPException(status_code=400, detail="Failed to read text content from the PDF")
        cv_content = "\n".join(full_text)

        matching_service = AIMatchingService()
        response = await matching_service.compute_matching(cv_content, offer)
        
        return response

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data processing (UUID or Parsing)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching processing failed: {str(e)}")
    finally:
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
