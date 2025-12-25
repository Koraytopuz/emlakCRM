from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.customer import Customer, Lead
from app.schemas.customer import CustomerCreate, CustomerUpdate, LeadCreate


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        db_customer = Customer(
            full_name=customer_data.full_name,
            email=customer_data.email,
            phone=customer_data.phone,
            company=customer_data.company,
            assigned_to_id=customer_data.assigned_to_id
        )
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def create_lead(self, lead_data: LeadCreate) -> Lead:
        """Lead kaydı oluştur ve müşteri skorunu güncelle"""
        db_lead = Lead(
            customer_id=lead_data.customer_id,
            source=lead_data.source,
            listing_id=lead_data.listing_id,
            action=lead_data.action,
            province=lead_data.province,
            district=lead_data.district,
            price_range_min=lead_data.price_range_min,
            price_range_max=lead_data.price_range_max
        )
        self.db.add(db_lead)
        self.db.commit()
        
        # Müşteri skorunu güncelle
        self.update_lead_score(lead_data.customer_id)
        
        return db_lead

    def update_lead_score(self, customer_id: int) -> Optional[Customer]:
        """Müşteri lead skorunu hesapla ve güncelle"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        # Basit skorlama algoritması (geliştirilebilir)
        score = 0.0
        
        # Lead aktivitelerine göre skor
        leads = self.db.query(Lead).filter(Lead.customer_id == customer_id).all()
        score += len(leads) * 5  # Her lead aktivitesi 5 puan
        
        # İlan görüntüleme sayısına göre
        if customer.viewed_listings:
            score += len(customer.viewed_listings) * 3
        
        # İletişim bilgileri tam ise
        if customer.email and customer.phone:
            score += 10
        
        # Maksimum 100 puan
        customer.lead_score = min(score, 100.0)
        
        self.db.commit()
        self.db.refresh(customer)
        return customer

