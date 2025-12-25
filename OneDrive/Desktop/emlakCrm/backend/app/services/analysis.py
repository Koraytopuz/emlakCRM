from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import math

from app.models.parcel import Parcel
from app.schemas.analysis import SlopeAnalysisResponse, POIAnalysisResponse


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_slope(self, parcel_id: int) -> Optional[SlopeAnalysisResponse]:
        """Parsel eğim analizi"""
        parcel = self.db.query(Parcel).filter(Parcel.id == parcel_id).first()
        if not parcel:
            return None
        
        # Eğer daha önce analiz yapılmışsa, kaydedilmiş veriyi kullan
        if parcel.slope_analysis:
            slope_data = parcel.slope_analysis
        else:
            # Örnek eğim analizi (gerçek implementasyon için DEM verisi gerekli)
            slope_data = self._calculate_slope(parcel)
            parcel.slope_analysis = slope_data
            self.db.commit()
        
        return SlopeAnalysisResponse(
            parcel_id=parcel_id,
            average_slope=slope_data.get("average", 5.0),
            max_slope=slope_data.get("max", 15.0),
            min_slope=slope_data.get("min", 0.0),
            slope_distribution=slope_data.get("distribution", {}),
            heatmap_data=slope_data.get("heatmap", []),
            suitability_score=slope_data.get("suitability", 85.0)
        )

    def _calculate_slope(self, parcel: Parcel) -> Dict[str, Any]:
        """Eğim hesaplama (örnek - gerçek implementasyon için DEM verisi gerekli)"""
        # Bu örnek implementasyon. Gerçek uygulamada:
        # 1. DEM (Digital Elevation Model) verisi kullanılmalı
        # 2. GeoPandas/Shapely ile eğim hesaplanmalı
        # 3. Raster veri işleme yapılmalı
        
        return {
            "average": 5.2,
            "max": 12.5,
            "min": 0.3,
            "distribution": {
                "0-5%": 60.0,
                "5-10%": 30.0,
                "10-15%": 8.0,
                "15%+": 2.0
            },
            "heatmap": [],  # Grid bazlı eğim verileri
            "suitability": 85.0  # İnşaat uygunluk skoru
        }

    def analyze_poi(self, parcel_id: int) -> Optional[POIAnalysisResponse]:
        """POI (Point of Interest) analizi"""
        parcel = self.db.query(Parcel).filter(Parcel.id == parcel_id).first()
        if not parcel:
            return None
        
        # Eğer daha önce analiz yapılmışsa, kaydedilmiş veriyi kullan
        if parcel.poi_distances:
            poi_data = parcel.poi_distances
        else:
            # POI mesafelerini hesapla (örnek - gerçek implementasyon için harita API'leri gerekli)
            poi_data = self._calculate_poi_distances(parcel)
            parcel.poi_distances = poi_data
            self.db.commit()
        
        return POIAnalysisResponse(
            parcel_id=parcel_id,
            distances=poi_data.get("distances", {}),
            poi_list=poi_data.get("poi_list", [])
        )

    def _calculate_poi_distances(self, parcel: Parcel) -> Dict[str, Any]:
        """POI mesafelerini hesapla (örnek - gerçek implementasyon için harita API'leri gerekli)"""
        # Gerçek uygulamada:
        # 1. Google Maps API veya OpenRouteService kullanılmalı
        # 2. Kuş uçuşu ve karayolu mesafeleri hesaplanmalı
        # 3. Önemli noktalar (hastane, okul, alışveriş merkezi) bulunmalı
        
        return {
            "distances": {
                "main_road": {"straight": 500, "road": 750},
                "city_center": {"straight": 2000, "road": 3500},
                "airport": {"straight": 15000, "road": 20000},
                "sea": {"straight": 5000, "road": 8000}
            },
            "poi_list": [
                {"name": "Ana Cadde", "type": "road", "distance": 500},
                {"name": "Şehir Merkezi", "type": "center", "distance": 2000}
            ]
        }

    def analyze_all(self, parcel_id: int) -> Optional[Dict[str, Any]]:
        """Tüm analizleri çalıştır"""
        slope_analysis = self.analyze_slope(parcel_id)
        poi_analysis = self.analyze_poi(parcel_id)
        
        if not slope_analysis or not poi_analysis:
            return None
        
        return {
            "parcel_id": parcel_id,
            "slope_analysis": slope_analysis.dict(),
            "poi_analysis": poi_analysis.dict()
        }

