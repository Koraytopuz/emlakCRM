from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ParcelSearch(BaseModel):
    province: Optional[str] = None
    district: Optional[str] = None
    block: Optional[str] = None
    parcel_number: Optional[str] = None


class ParcelCreate(BaseModel):
    province: str
    district: str
    neighborhood: Optional[str] = None
    block: str
    parcel_number: str
    geometry: Dict[str, Any]  # GeoJSON format
    area_m2: float
    center_lat: float
    center_lon: float
    zoning_status: Optional[str] = None
    zoning_code: Optional[str] = None
    source: Optional[str] = None
    source_id: Optional[str] = None


class ParcelResponse(BaseModel):
    id: int
    province: str
    district: str
    neighborhood: Optional[str]
    block: str
    parcel_number: str
    area_m2: float
    center_lat: float
    center_lon: float
    slope_analysis: Optional[Dict[str, Any]]
    elevation_data: Optional[Dict[str, Any]]
    poi_distances: Optional[Dict[str, Any]]
    zoning_status: Optional[str]
    zoning_code: Optional[str]
    building_rights: Optional[Dict[str, Any]]
    created_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True

