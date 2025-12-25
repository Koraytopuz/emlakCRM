from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analysis import SlopeAnalysisResponse, POIAnalysisResponse
from app.services.analysis import AnalysisService

router = APIRouter()


@router.get("/parcels/{parcel_id}/slope", response_model=SlopeAnalysisResponse)
async def analyze_slope(
    parcel_id: int,
    db: Session = Depends(get_db)
):
    """Parsel eğim analizi"""
    service = AnalysisService(db)
    analysis = service.analyze_slope(parcel_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Parsel bulunamadı")
    return analysis


@router.get("/parcels/{parcel_id}/poi", response_model=POIAnalysisResponse)
async def analyze_poi(
    parcel_id: int,
    db: Session = Depends(get_db)
):
    """Parsel POI (Point of Interest) analizi"""
    service = AnalysisService(db)
    analysis = service.analyze_poi(parcel_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Parsel bulunamadı")
    return analysis


@router.post("/parcels/{parcel_id}/analyze-all")
async def analyze_all(
    parcel_id: int,
    db: Session = Depends(get_db)
):
    """Parsel için tüm analizleri çalıştır (eğim + POI)"""
    service = AnalysisService(db)
    result = service.analyze_all(parcel_id)
    if not result:
        raise HTTPException(status_code=404, detail="Parsel bulunamadı")
    return result

