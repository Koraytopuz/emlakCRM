from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class DroneWaypoint(BaseModel):
    """Drone turu waypoint (duraklama noktası)"""
    longitude: float
    latitude: float
    height: float  # Yükseklik (metre)
    heading: Optional[float] = None  # Bakış açısı (derece)
    pitch: Optional[float] = None  # Eğim açısı (derece)
    roll: Optional[float] = None  # Yatış açısı (derece)
    duration: Optional[float] = None  # Bu noktada kalma süresi (saniye)
    speed: Optional[float] = None  # Bu segment için hız (m/s)


class AtmosphereSettings(BaseModel):
    """Atmosfer ayarları"""
    sun_angle: float = 45.0  # Güneş açısı (derece)
    time_of_day: str = "12:00"  # Saat (HH:MM formatında)
    cloud_density: float = 0.3  # Bulut yoğunluğu (0-1)
    fog_density: float = 0.0  # Sis yoğunluğu (0-1)


class DroneTourRequest(BaseModel):
    """Drone turu yapılandırması"""
    tour_type: str = "autonomous"  # "autonomous", "orbit", "poi", "topographic"
    flight_mode: str = "orbit"  # "orbit", "poi", "topographic_slice"
    altitude: float = 100.0  # Ortalama yükseklik (metre)
    speed: float = 5.0  # Ortalama hız (m/s)
    waypoints: Optional[List[DroneWaypoint]] = None  # Özel waypoint'ler
    auto_generate: bool = True  # Otomatik rota oluştur
    include_edges: bool = True  # Parsel kenarlarını dahil et
    include_center: bool = True  # Merkez noktayı dahil et
    number_of_points: int = 8  # Otomatik oluşturulacak nokta sayısı
    orbit_radius: Optional[float] = None  # Orbit modu için yarıçap (metre)
    orbit_height: Optional[float] = None  # Orbit modu için yükseklik (metre)
    poi_targets: Optional[List[Dict[str, Any]]] = None  # POI modu için hedefler
    atmosphere: Optional[AtmosphereSettings] = None  # Atmosfer ayarları
    use_bezier: bool = True  # Bezier eğrileri kullan
    enable_ar_lines: bool = True  # AR sınır çizgileri
    enable_info_labels: bool = True  # Bilgi etiketleri
    enable_compass: bool = True  # Pusula


class VirtualBuilding(BaseModel):
    """Sanal bina modeli"""
    longitude: float
    latitude: float
    height: float  # Bina yüksekliği (metre)
    width: float  # Genişlik (metre)
    length: float  # Uzunluk (metre)
    rotation: float = 0.0  # Rotasyon (derece)
    model_type: str = "villa"  # "villa", "apartment", "commercial"
    floor_count: int = 2  # Kat sayısı


class DroneTourResponse(BaseModel):
    """Drone turu yanıtı"""
    parcel_id: int
    tour_type: str
    flight_mode: str
    waypoints: List[Dict[str, Any]]
    bezier_control_points: Optional[List[Dict[str, Any]]] = None  # Bezier kontrol noktaları
    total_duration: float  # Toplam tur süresi (saniye)
    total_distance: float  # Toplam mesafe (metre)
    metadata: Dict[str, Any]
    shareable_link: Optional[str] = None  # Paylaşılabilir link


class VideoExportRequest(BaseModel):
    """Video export isteği"""
    parcel_id: int
    tour_id: Optional[str] = None
    resolution: str = "1920x1080"  # "1920x1080", "1280x720", "3840x2160"
    duration: Optional[float] = None  # Video süresi (saniye), None ise tam tur
    fps: int = 30  # Frame per second
    quality: str = "high"  # "low", "medium", "high"


class VideoExportResponse(BaseModel):
    """Video export yanıtı"""
    video_id: str
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: float
    file_size: int  # Byte cinsinden
    status: str  # "processing", "completed", "failed"
