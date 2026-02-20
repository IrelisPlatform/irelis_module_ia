from typing import Annotated, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status

from app.schemas.dtos import JobOfferDto
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
    text: str
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