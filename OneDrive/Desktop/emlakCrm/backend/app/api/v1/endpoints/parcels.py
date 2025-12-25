from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.parcel import ParcelResponse, ParcelCreate, ParcelSearch
from app.services.parcel import ParcelService
from app.models.parcel import Parcel

router = APIRouter()


# ÖNEMLİ: /search route'u /{parcel_id} route'undan ÖNCE tanımlanmalı
# Aksi halde FastAPI "search" string'ini parcel_id olarak yorumlar
@router.post("/search", response_model=List[ParcelResponse])
async def search_parcels(
    search: ParcelSearch,
    db: Session = Depends(get_db)
):
    """Parsel sorgulama (İl/İlçe/Ada/Parsel bazlı)"""
    import logging
    import sys
    logger = logging.getLogger(__name__)
    
    # Debug: Gelen parametreleri logla (hem logger hem print)
    search_dict = search.model_dump()
    print(f"[DEBUG Parcels Endpoint] Search endpoint called with params: {search_dict}", file=sys.stderr)
    print(f"[DEBUG Parcels Endpoint] Block type: {type(search_dict.get('block'))}, value: '{search_dict.get('block')}'", file=sys.stderr)
    print(f"[DEBUG Parcels Endpoint] Parcel_number type: {type(search_dict.get('parcel_number'))}, value: '{search_dict.get('parcel_number')}'", file=sys.stderr)
    logger.info(f"Search params: {search_dict}")
    
    service = ParcelService(db)
    
    # Veritabanındaki toplam parsel sayısını kontrol et
    try:
        from app.models.parcel import Parcel
        total_parcels = db.query(Parcel).count()
        print(f"[DEBUG Parcels Endpoint] Veritabanındaki toplam parsel sayısı: {total_parcels}", file=sys.stderr)
    except Exception as e:
        print(f"[DEBUG Parcels Endpoint] Parsel sayısı kontrol edilemedi: {e}", file=sys.stderr)
    
    parcels = service.search_parcels(search)
    
    # Debug: Bulunan parsel sayısını logla
    print(f"[DEBUG Parcels Endpoint] Found {len(parcels)} parcels", file=sys.stderr)
    logger.info(f"Found {len(parcels)} parcels")
    
    return parcels


@router.get("/{parcel_id}", response_model=ParcelResponse)
async def get_parcel(
    parcel_id: int,
    db: Session = Depends(get_db)
):
    """Parsel detayları"""
    service = ParcelService(db)
    parcel = service.get_parcel_by_id(parcel_id)
    if not parcel:
        raise HTTPException(status_code=404, detail="Parsel bulunamadı")
    return parcel


@router.post("/", response_model=ParcelResponse, status_code=201)
async def create_parcel(
    parcel_data: ParcelCreate,
    db: Session = Depends(get_db)
):
    """Yeni parsel kaydı oluştur"""
    service = ParcelService(db)
    parcel = service.create_parcel(parcel_data)
    return parcel


@router.get("/{parcel_id}/geometry")
async def get_parcel_geometry(
    parcel_id: int,
    format: str = Query(default="geojson", regex="^(geojson|wkt)$"),
    db: Session = Depends(get_db)
):
    """Parsel geometrisini al (GeoJSON veya WKT formatında)"""
    service = ParcelService(db)
    geometry = service.get_parcel_geometry(parcel_id, format)
    if not geometry:
        raise HTTPException(status_code=404, detail="Parsel bulunamadı")
    return geometry

