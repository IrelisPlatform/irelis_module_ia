from __future__ import annotations

from typing import Annotated
from uuid import UUID
import os

from app.models.entities import JobOffer
from app.services.ai.ai_matchind_service import AIMatchingService
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
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
    link: str = Query(..., alias="link to the job offer"),
    file: UploadFile = File(...)
):
    """Return the semantic matching percentage and breakdown between a cv and a job offer using AI."""
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
        
    try:
        # 1. Extraction de l'UUID
        if "irelis.net/jobs/" in link:
            job_offer_id = UUID(link[-36:])  # On prend les 36 derniers caractères pour l'UUID
        else:
            raise HTTPException(status_code=400, detail="Invalid job offer link format")

        # 2. Récupération de l'offre en Base de Données (avec SQLAlchemy)
        offer = db.query(JobOffer).filter(JobOffer.id == job_offer_id).first()
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer Not Found")

        # 3. Extraction du texte du PDF
        reader = PdfReader(file.file)
        full_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        if not full_text:
            raise HTTPException(status_code=400, detail="Failed to read text content from the PDF")
        
        cv_content = "\n".join(full_text)

        # 4. Appel de l'IA pour le matching sémantique
        matching_service = AIMatchingService(ai_client)
        response = await matching_service.compute_matching(cv_content, offer)
        
        return response

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID in the link")
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
