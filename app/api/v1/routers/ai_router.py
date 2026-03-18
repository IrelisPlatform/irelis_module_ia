from typing import Annotated, Optional
from app.services.ai.scraping_service import WebScrapingService
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status

from app.schemas.dtos import JobOfferDto, ScrapeRequest
from app.services.ai.ai_extraction_service import AIExtractionService

router = APIRouter(prefix="/ai", tags=["AI Extraction"])

@router.post("/extract-job-offer/file", response_model=JobOfferDto)
async def extract_job_offer_file(
    file: UploadFile = File(...) 
) -> JobOfferDto:
    """
    Extract all information about job_offer from text, image or pdf
    """
    try:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Please provide a file."
            )
            
        if file and file.content_type not in ["application/pdf", "image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Do not support this format. Use PDF, JPEG, PNG ou WEBP."
            )

        ai_service = AIExtractionService()
        extracted_offer = await ai_service.extract_from_payload_file( file)
        
        return extracted_offer

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/extract-job-offer/text", response_model=JobOfferDto)
async def extract_job_offer_text(
    text: str = Form(...)
) -> JobOfferDto:
    """
    Extract all information about job_offer from text
    """
    try:
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Please provide a text."
            )
        

        ai_service = AIExtractionService()
        extracted_offer = await ai_service.extract_from_payload_text(text)
        
        return extracted_offer

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/scrapping/url", response_model=list[JobOfferDto])
async def scrape_jobs_from_url(request: ScrapeRequest) -> list[JobOfferDto]:
    """
    Scrape une page web d'entreprise et retourne toutes les offres d'emploi trouvées.
    Exemple de payload: {"url": "https://www.enterprise.cm/fr/carrieres.html"}
    """
    try:
        # Pydantic valide l'URL automatiquement, on doit juste la convertir en string
        url_str = str(request.url) 
        
        scraper = WebScrapingService()
        offers = await scraper.scrape_offers_list(url_str)
        
        return offers

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))