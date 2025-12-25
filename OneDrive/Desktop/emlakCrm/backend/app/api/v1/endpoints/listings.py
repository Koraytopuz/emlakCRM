from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.listing import ListingResponse, ListingCreate, ListingUpdate
from app.services.listing import ListingService

router = APIRouter()


@router.get("/", response_model=List[ListingResponse])
async def get_listings(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    """İlan listesi"""
    service = ListingService(db)
    listings = service.get_listings(skip=skip, limit=limit, status=status)
    return listings


@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """İlan detayları"""
    service = ListingService(db)
    listing = service.get_listing_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return listing


@router.post("/", response_model=ListingResponse, status_code=201)
async def create_listing(
    listing_data: ListingCreate,
    db: Session = Depends(get_db)
):
    """Yeni ilan oluştur"""
    service = ListingService(db)
    listing = service.create_listing(listing_data)
    return listing


@router.put("/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: int,
    listing_data: ListingUpdate,
    db: Session = Depends(get_db)
):
    """İlan güncelle"""
    service = ListingService(db)
    listing = service.update_listing(listing_id, listing_data)
    if not listing:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return listing


@router.delete("/{listing_id}", status_code=204)
async def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """İlan sil"""
    service = ListingService(db)
    success = service.delete_listing(listing_id)
    if not success:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")

