from pydantic import BaseModel
from typing import Dict, Any, List


class SlopeAnalysisResponse(BaseModel):
    parcel_id: int
    average_slope: float  # Yüzde cinsinden ortalama eğim
    max_slope: float
    min_slope: float
    slope_distribution: Dict[str, float]  # Eğim kategorileri ve yüzdeleri
    heatmap_data: List[Dict[str, Any]]  # Isı haritası verileri
    suitability_score: float  # İnşaat uygunluk skoru (0-100)


class POIAnalysisResponse(BaseModel):
    parcel_id: int
    distances: Dict[str, Dict[str, float]]  # {"main_road": {"straight": 500, "road": 750}, ...}
    poi_list: List[Dict[str, Any]]  # Detaylı POI listesi

