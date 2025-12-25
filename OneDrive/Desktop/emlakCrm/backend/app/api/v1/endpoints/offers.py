from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.offer import OfferResponse, OfferCreate, ContractResponse, ContractCreate
from app.services.offer import OfferService

router = APIRouter()


@router.get("/", response_model=List[OfferResponse])
async def get_offers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Teklif listesi"""
    service = OfferService(db)
    offers = service.get_offers(skip=skip, limit=limit)
    return offers


@router.post("/", response_model=OfferResponse, status_code=201)
async def create_offer(
    offer_data: OfferCreate,
    db: Session = Depends(get_db)
):
    """Yeni teklif oluştur"""
    service = OfferService(db)
    offer = service.create_offer(offer_data)
    return offer


@router.post("/{offer_id}/contract", response_model=ContractResponse, status_code=201)
async def create_contract(
    offer_id: int,
    contract_data: ContractCreate,
    db: Session = Depends(get_db)
):
    """Teklif için sözleşme oluştur"""
    service = OfferService(db)
    contract = service.create_contract(offer_id, contract_data)
    if not contract:
        raise HTTPException(status_code=404, detail="Teklif bulunamadı")
    return contract

