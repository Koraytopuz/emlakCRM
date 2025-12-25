from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="listings")
    
    # Parsel bağlantısı
    parcel_id = Column(Integer, ForeignKey("parcels.id"), nullable=False)
    parcel = relationship("Parcel", back_populates="listings")
    
    # İlan bilgileri
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    ai_generated_description = Column(Text, nullable=True)  # AI ile oluşturulan açıklama
    
    # Fiyat
    price = Column(Float, nullable=False)
    currency = Column(String, default="TRY")
    
    # Durum
    status = Column(String, default="draft")  # draft, active, sold, archived
    is_featured = Column(Boolean, default=False)
    
    # Pazarlama
    marketing_tags = Column(JSON, nullable=True)  # ["deniz manzarası", "şehir merkezi", vb.]
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    
    # Medya
    images = Column(JSON, nullable=True)  # Image URLs array
    videos = Column(JSON, nullable=True)  # Video URLs array
    drone_tour_url = Column(String, nullable=True)  # 3D tour URL
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    offers = relationship("Offer", back_populates="listing")

