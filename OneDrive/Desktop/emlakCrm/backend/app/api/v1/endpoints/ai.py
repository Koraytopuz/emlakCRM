from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai import ListingDescriptionRequest, ListingDescriptionResponse
from app.services.ai import AIService

router = APIRouter()


@router.post("/generate-listing-description", response_model=ListingDescriptionResponse)
async def generate_listing_description(
    request: ListingDescriptionRequest,
    db: Session = Depends(get_db)
):
    """AI ile ilan açıklaması oluştur"""
    service = AIService(db)
    description = service.generate_listing_description(
        listing_id=request.listing_id,
        style=request.style,
        language=request.language
    )
    if not description:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return {"description": description}

