from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.listing import Listing
from app.schemas.listing import ListingCreate, ListingUpdate


class ListingService:
    def __init__(self, db: Session):
        self.db = db

    def get_listings(self, skip: int = 0, limit: int = 100, status: str = None) -> List[Listing]:
        query = self.db.query(Listing)
        if status:
            query = query.filter(Listing.status == status)
        return query.offset(skip).limit(limit).all()

    def get_listing_by_id(self, listing_id: int) -> Optional[Listing]:
        listing = self.db.query(Listing).filter(Listing.id == listing_id).first()
        if listing:
            listing.view_count += 1
            self.db.commit()
        return listing

    def create_listing(self, listing_data: ListingCreate, owner_id: int = None) -> Listing:
        db_listing = Listing(
            owner_id=owner_id or listing_data.owner_id or 1,  # Auth'dan gelen owner_id kullanılmalı
            parcel_id=listing_data.parcel_id,
            title=listing_data.title,
            description=listing_data.description,
            price=listing_data.price,
            currency=listing_data.currency,
            status=listing_data.status,
            marketing_tags=listing_data.marketing_tags,
            images=listing_data.images
        )
        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return db_listing

    def update_listing(self, listing_id: int, listing_data: ListingUpdate) -> Optional[Listing]:
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            return None
        
        update_data = listing_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(listing, field, value)
        
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def delete_listing(self, listing_id: int) -> bool:
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            return False
        self.db.delete(listing)
        self.db.commit()
        return True

