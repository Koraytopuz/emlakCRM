from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.core.database import Base


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    
    # Parsel bilgileri
    province = Column(String, nullable=False, index=True)  # İl
    district = Column(String, nullable=False, index=True)  # İlçe
    neighborhood = Column(String, nullable=True)  # Mahalle
    block = Column(String, nullable=False)  # Ada
    parcel_number = Column(String, nullable=False)  # Parsel
    
    # Coğrafi veriler
    geometry = Column(Geometry('POLYGON', srid=4326), nullable=False)  # PostGIS geometry
    area_m2 = Column(Float, nullable=False)  # Alan (m²)
    center_lat = Column(Float, nullable=False)  # Merkez enlem
    center_lon = Column(Float, nullable=False)  # Merkez boylam
    
    # Analiz verileri
    slope_analysis = Column(JSON, nullable=True)  # Eğim analizi verileri
    elevation_data = Column(JSON, nullable=True)  # Yükselti verileri
    poi_distances = Column(JSON, nullable=True)  # POI mesafeleri
    
    # İmar ve yasal bilgiler
    zoning_status = Column(String, nullable=True)  # İmar durumu
    zoning_code = Column(String, nullable=True)  # İmar kodu
    building_rights = Column(JSON, nullable=True)  # Yapı hakları
    
    # Metadata
    source = Column(String, nullable=True)  # Veri kaynağı (TKGM, vb.)
    source_id = Column(String, nullable=True)  # Kaynak sistem ID
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    listings = relationship("Listing", back_populates="parcel")

