from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class OfferCreate(BaseModel):
    listing_id: int
    customer_id: int
    offer_amount: float
    currency: str = "TRY"
    conditions: Optional[str] = None
    payment_plan: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None


class OfferResponse(BaseModel):
    id: int
    listing_id: int
    customer_id: int
    offer_amount: float
    currency: str
    status: str
    conditions: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True


class ContractCreate(BaseModel):
    contract_type: str
    contract_terms: Dict[str, Any]


class ContractResponse(BaseModel):
    id: int
    offer_id: int
    contract_number: str
    contract_type: str
    status: str
    signed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

