from pydantic import BaseModel
from typing import Optional


class ListingDescriptionRequest(BaseModel):
    listing_id: int
    style: Optional[str] = "professional"  # professional, casual, luxury
    language: Optional[str] = "tr"  # tr, en


class ListingDescriptionResponse(BaseModel):
    description: str

