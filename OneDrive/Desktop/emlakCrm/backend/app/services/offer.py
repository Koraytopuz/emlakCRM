from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.models.offer import Offer, Contract
from app.schemas.offer import OfferCreate, ContractCreate


class OfferService:
    def __init__(self, db: Session):
        self.db = db

    def get_offers(self, skip: int = 0, limit: int = 100) -> List[Offer]:
        return self.db.query(Offer).offset(skip).limit(limit).all()

    def create_offer(self, offer_data: OfferCreate) -> Offer:
        db_offer = Offer(
            listing_id=offer_data.listing_id,
            customer_id=offer_data.customer_id,
            offer_amount=offer_data.offer_amount,
            currency=offer_data.currency,
            conditions=offer_data.conditions,
            payment_plan=offer_data.payment_plan,
            expires_at=offer_data.expires_at
        )
        self.db.add(db_offer)
        self.db.commit()
        self.db.refresh(db_offer)
        return db_offer

    def create_contract(self, offer_id: int, contract_data: ContractCreate) -> Optional[Contract]:
        """Teklif için sözleşme oluştur"""
        offer = self.db.query(Offer).filter(Offer.id == offer_id).first()
        if not offer:
            return None
        
        # Benzersiz sözleşme numarası oluştur
        contract_number = f"CNT-{uuid.uuid4().hex[:8].upper()}"
        
        db_contract = Contract(
            offer_id=offer_id,
            contract_number=contract_number,
            contract_type=contract_data.contract_type,
            contract_terms=contract_data.contract_terms
        )
        self.db.add(db_contract)
        self.db.commit()
        self.db.refresh(db_contract)
        return db_contract

