from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ListingCreate(BaseModel):
    parcel_id: int
    owner_id: Optional[int] = None  # Auth'dan alınacak
    title: str
    description: Optional[str] = None
    price: float
    currency: str = "TRY"
    status: str = "draft"
    marketing_tags: Optional[List[str]] = None
    images: Optional[List[str]] = None


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[str] = None
    marketing_tags: Optional[List[str]] = None
    images: Optional[List[str]] = None


class ListingResponse(BaseModel):
    id: int
    owner_id: int
    parcel_id: int
    title: str
    description: Optional[str]
    ai_generated_description: Optional[str]
    price: float
    currency: str
    status: str
    is_featured: bool
    marketing_tags: Optional[List[str]]
    view_count: int
    favorite_count: int
    images: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

