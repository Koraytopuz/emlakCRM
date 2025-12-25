from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.schemas.drone import (
    DroneTourRequest, 
    DroneTourResponse, 
    DroneWaypoint,
    VideoExportRequest,
    VideoExportResponse
)
from app.services.drone import DroneTourService
from app.services.video_export import VideoExportService

router = APIRouter()


@router.post("/parcels/{parcel_id}/tour", response_model=DroneTourResponse)
async def create_drone_tour(
    parcel_id: int,
    tour_config: DroneTourRequest,
    db: Session = Depends(get_db)
):
    """Parsel için sanal drone turu rotası oluştur"""
    service = DroneTourService(db)
    tour = service.create_drone_tour(parcel_id, tour_config)
    if not tour:
        raise HTTPException(status_code=404, detail="Parsel bulunamadı")
    return tour


@router.get("/parcels/{parcel_id}/tour", response_model=DroneTourResponse)
async def get_drone_tour(
    parcel_id: int,
    db: Session = Depends(get_db)
):
    """Mevcut drone turu rotasını al"""
    service = DroneTourService(db)
    tour = service.get_drone_tour(parcel_id)
    if not tour:
        raise HTTPException(status_code=404, detail="Drone turu bulunamadı")
    return tour


@router.get("/tour/{tour_id}")
async def get_shareable_tour(
    tour_id: str,
    db: Session = Depends(get_db)
):
    """Paylaşılabilir link ile tur bilgilerini al"""
    # TODO: Tour ID'den parsel ID'yi bul ve turu döndür
    # Şimdilik basit bir implementasyon
    return {"tour_id": tour_id, "message": "Tour data will be loaded"}


@router.post("/video/export", response_model=VideoExportResponse)
async def export_video(
    export_request: VideoExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Drone turunu video olarak export et"""
    service = VideoExportService(db)
    video_export = service.create_video_export(export_request)
    
    # Arka planda video render işlemini başlat
    background_tasks.add_task(service.render_video, video_export.video_id)
    
    return video_export


@router.get("/video/{video_id}", response_model=VideoExportResponse)
async def get_video_status(
    video_id: str,
    db: Session = Depends(get_db)
):
    """Video export durumunu kontrol et"""
    service = VideoExportService(db)
    video = service.get_video_export(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video bulunamadı")
    return video

