from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True, index=True)
    company = Column(String, nullable=True)
    
    # Lead scoring
    lead_score = Column(Float, default=0.0)  # 0-100 arası skor
    interest_areas = Column(JSON, nullable=True)  # İlgilendiği bölgeler
    viewed_listings = Column(JSON, nullable=True)  # Görüntülediği ilanlar
    
    # Assignment
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to = relationship("User", back_populates="customers")
    
    # Status
    status = Column(String, default="new")  # new, contacted, qualified, converted, lost
    notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    leads = relationship("Lead", back_populates="customer")
    offers = relationship("Offer", back_populates="customer")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="leads")
    
    # Lead activity
    source = Column(String, nullable=True)  # website, referral, social, etc.
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=True)
    action = Column(String, nullable=False)  # viewed, contacted, favorited, etc.
    
    # Location interest
    province = Column(String, nullable=True)
    district = Column(String, nullable=True)
    price_range_min = Column(Float, nullable=True)
    price_range_max = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

