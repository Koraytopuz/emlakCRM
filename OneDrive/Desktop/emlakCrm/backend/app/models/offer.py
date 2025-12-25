from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    
    # İlişkiler
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    listing = relationship("Listing", back_populates="offers")
    
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="offers")
    
    # Teklif bilgileri
    offer_amount = Column(Float, nullable=False)
    currency = Column(String, default="TRY")
    status = Column(String, default="pending")  # pending, accepted, rejected, withdrawn
    
    # Şartlar
    conditions = Column(Text, nullable=True)
    payment_plan = Column(JSON, nullable=True)  # Ödeme planı
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    contract = relationship("Contract", back_populates="offer", uselist=False)


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    
    # İlişkiler
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False, unique=True)
    offer = relationship("Offer", back_populates="contract")
    
    # Sözleşme bilgileri
    contract_number = Column(String, unique=True, nullable=False)
    contract_type = Column(String, nullable=False)  # sale, rent, etc.
    
    # Dijital imza
    seller_signature = Column(Text, nullable=True)  # Base64 encoded signature
    buyer_signature = Column(Text, nullable=True)
    signed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Sözleşme içeriği
    contract_terms = Column(JSON, nullable=False)  # Sözleşme maddeleri
    contract_pdf_url = Column(String, nullable=True)  # Oluşturulan PDF URL
    
    # Durum
    status = Column(String, default="draft")  # draft, signed, executed, cancelled
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

