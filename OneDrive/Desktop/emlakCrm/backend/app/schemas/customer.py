from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class CustomerCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    assigned_to_id: Optional[int] = None


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    lead_score: float
    interest_areas: Optional[Dict[str, Any]]
    status: str
    assigned_to_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class LeadCreate(BaseModel):
    customer_id: int
    source: Optional[str] = None
    listing_id: Optional[int] = None
    action: str
    province: Optional[str] = None
    district: Optional[str] = None
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None

