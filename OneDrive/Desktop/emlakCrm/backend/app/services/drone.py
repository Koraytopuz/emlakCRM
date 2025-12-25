from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import math
import uuid
from shapely.geometry import shape, Point, Polygon
from shapely.ops import unary_union

from app.models.parcel import Parcel
from app.schemas.drone import (
    DroneTourRequest, 
    DroneTourResponse, 
    DroneWaypoint,
    AtmosphereSettings,
    VirtualBuilding
)


class DroneTourService:
    def __init__(self, db: Session):
        self.db = db

    def create_drone_tour(
        self,
        parcel_id: int,
        tour_config: DroneTourRequest
    ) -> Optional[DroneTourResponse]:
        """Parsel için drone turu rotası oluştur"""
        parcel = self.db.query(Parcel).filter(Parcel.id == parcel_id).first()
        if not parcel:
            return None

        # Parsel geometrisini al
        shapely_geom = self._get_parcel_geometry(parcel)

        # Uçuş moduna göre rota oluştur
        if tour_config.flight_mode == "orbit":
            waypoints, bezier_points = self._generate_orbit_route(
                shapely_geom, parcel, tour_config
            )
        elif tour_config.flight_mode == "poi":
            waypoints, bezier_points = self._generate_poi_route(
                shapely_geom, parcel, tour_config
            )
        elif tour_config.flight_mode == "topographic_slice":
            waypoints, bezier_points = self._generate_topographic_route(
                shapely_geom, parcel, tour_config
            )
        else:
            # Varsayılan: autonomous
            waypoints, bezier_points = self._generate_autonomous_route(
                shapely_geom, parcel, tour_config
            )

        # Tur metadata'sını hesapla
        total_distance = self._calculate_total_distance(waypoints)
        total_duration = total_distance / tour_config.speed if tour_config.speed > 0 else 0

        # Paylaşılabilir link oluştur
        tour_id = str(uuid.uuid4())
        shareable_link = f"/drone-tour/{tour_id}"

        return DroneTourResponse(
            parcel_id=parcel_id,
            tour_type=tour_config.tour_type,
            flight_mode=tour_config.flight_mode,
            waypoints=waypoints,
            bezier_control_points=bezier_points if tour_config.use_bezier else None,
            total_duration=total_duration,
            total_distance=total_distance,
            metadata={
                "altitude": tour_config.altitude,
                "speed": tour_config.speed,
                "parcel_area": parcel.area_m2,
                "center": {
                    "lat": parcel.center_lat,
                    "lon": parcel.center_lon
                },
                "atmosphere": tour_config.atmosphere.dict() if tour_config.atmosphere else None,
                "enable_ar_lines": tour_config.enable_ar_lines,
                "enable_info_labels": tour_config.enable_info_labels,
                "enable_compass": tour_config.enable_compass,
            },
            shareable_link=shareable_link
        )

    def _get_parcel_geometry(self, parcel: Parcel) -> Polygon:
        """Parsel geometrisini Shapely Polygon'a dönüştür"""
        geom = parcel.geometry
        try:
            if hasattr(geom, '__geo_interface__'):
                geo_dict = geom.__geo_interface__
                return shape(geo_dict)
            elif hasattr(geom, 'wkt'):
                from shapely import wkt
                return wkt.loads(geom.wkt)
            else:
                from shapely import wkt
                return wkt.loads(str(geom))
        except Exception as e:
            print(f"Geometry conversion error: {e}")
            # Fallback: Basit bounding box
            center = Point(parcel.center_lon, parcel.center_lat)
            size = math.sqrt(parcel.area_m2) / 111320
            return center.buffer(size)

    def _generate_orbit_route(
        self,
        geometry: Polygon,
        parcel: Parcel,
        config: DroneTourRequest
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Orbit (Yörünge) modu: Parsel merkezi etrafında 360° tur"""
        center = geometry.centroid
        orbit_radius = config.orbit_radius or (math.sqrt(parcel.area_m2 / math.pi) * 1.5)
        orbit_height = config.orbit_height or config.altitude

        waypoints = []
        bezier_points = []

        # 360° tur için waypoint'ler
        num_points = max(16, config.number_of_points * 2)  # Daha pürüzsüz için daha fazla nokta
        
        for i in range(num_points + 1):
            angle = (2 * math.pi * i) / num_points
            lon = center.x + (orbit_radius / 111320) * math.cos(angle)
            lat = center.y + (orbit_radius / 111320) * math.sin(angle)
            
            # Parsel merkezine bakış açısı
            heading = math.degrees(angle + math.pi)  # Merkeze bakış
            
            waypoint = {
                "longitude": lon,
                "latitude": lat,
                "height": orbit_height,
                "heading": heading,
                "pitch": -30,  # 30° aşağı bakış
                "roll": 0,
                "duration": 0.5,
                "speed": config.speed
            }
            waypoints.append(waypoint)

            # Bezier kontrol noktaları (her waypoint için)
            if config.use_bezier and i < num_points:
                # Önceki, mevcut ve sonraki nokta arasında bezier
                next_angle = (2 * math.pi * (i + 1)) / num_points
                next_lon = center.x + (orbit_radius / 111320) * math.cos(next_angle)
                next_lat = center.y + (orbit_radius / 111320) * math.sin(next_angle)
                
                bezier_points.append({
                    "p0": {"lon": lon, "lat": lat, "height": orbit_height},
                    "p1": {
                        "lon": (lon + next_lon) / 2,
                        "lat": (lat + next_lat) / 2,
                        "height": orbit_height
                    },
                    "p2": {"lon": next_lon, "lat": next_lat, "height": orbit_height}
                })

        return waypoints, bezier_points

    def _generate_poi_route(
        self,
        geometry: Polygon,
        parcel: Parcel,
        config: DroneTourRequest
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """POI (Points of Interest) modu: Önemli noktalara fly-over"""
        center = geometry.centroid
        waypoints = []
        bezier_points = []

        # Parsel merkezinden başla
        waypoints.append({
            "longitude": center.x,
            "latitude": center.y,
            "height": config.altitude * 1.5,
            "heading": 0,
            "pitch": -90,
            "duration": 2.0,
            "speed": config.speed
        })

        # POI hedefleri (parsel POI analizinden veya manuel)
        poi_targets = config.poi_targets or []
        
        if not poi_targets and parcel.poi_distances:
            # Parsel POI verilerinden hedefler oluştur
            poi_data = parcel.poi_distances
            if isinstance(poi_data, dict) and "distances" in poi_data:
                for poi_name, distances in poi_data["distances"].items():
                    # Basit hedef oluştur (gerçek uygulamada harita API'den alınmalı)
                    target_lon = center.x + (distances.get("straight", 1000) / 111320) * 0.5
                    target_lat = center.y + (distances.get("straight", 1000) / 111320) * 0.5
                    
                    poi_targets.append({
                        "name": poi_name,
                        "longitude": target_lon,
                        "latitude": target_lat,
                        "distance": distances.get("straight", 1000)
                    })

        # Her POI için fly-over
        for poi in poi_targets[:5]:  # Maksimum 5 POI
            # POI'ye doğru uçuş
            waypoints.append({
                "longitude": poi["longitude"],
                "latitude": poi["latitude"],
                "height": config.altitude * 2,
                "heading": self._calculate_heading(
                    center.x, center.y,
                    poi["longitude"], poi["latitude"]
                ),
                "pitch": -45,
                "duration": 3.0,
                "speed": config.speed * 1.5
            })

            # Parsel merkezine geri dönüş
            waypoints.append({
                "longitude": center.x,
                "latitude": center.y,
                "height": config.altitude,
                "heading": self._calculate_heading(
                    poi["longitude"], poi["latitude"],
                    center.x, center.y
                ),
                "pitch": -60,
                "duration": 3.0,
                "speed": config.speed
            })

        return waypoints, bezier_points

    def _generate_topographic_route(
        self,
        geometry: Polygon,
        parcel: Parcel,
        config: DroneTourRequest
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Topographic Slice modu: Yatay kesit görünümü"""
        center = geometry.centroid
        bounds = geometry.bounds
        min_lon, min_lat, max_lon, max_lat = bounds

        waypoints = []
        bezier_points = []

        # Göz hizası yüksekliği (yaklaşık 1.7m)
        eye_level = 1.7

        # Parsel boyunca yatay kesit
        num_slices = 8
        for i in range(num_slices + 1):
            t = i / num_slices
            lon = min_lon + (max_lon - min_lon) * t
            lat = min_lat + (max_lat - min_lat) * t

            # Yatay bakış (pitch = 0)
            waypoints.append({
                "longitude": lon,
                "latitude": lat,
                "height": eye_level,
                "heading": 90 * (i % 4),  # Farklı yönlere bakış
                "pitch": 0,  # Yatay
                "roll": 0,
                "duration": 2.0,
                "speed": config.speed * 0.5  # Yavaş hareket
            })

        return waypoints, bezier_points

    def _generate_autonomous_route(
        self,
        geometry: Polygon,
        parcel: Parcel,
        config: DroneTourRequest
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Otonom rota (eski implementasyon)"""
        waypoints = []
        points_to_visit = []
        center = geometry.centroid
        coords = list(geometry.exterior.coords)

        # Merkez nokta
        if config.include_center:
            points_to_visit.append({
                "lon": center.x,
                "lat": center.y,
                "height": config.altitude * 1.5,
                "heading": 0,
                "pitch": -90,
                "duration": 3.0
            })

        # Köşe noktaları
        if config.include_edges:
            for i, (lon, lat) in enumerate(coords[:-1]):
                points_to_visit.append({
                    "lon": lon,
                    "lat": lat,
                    "height": config.altitude,
                    "heading": self._calculate_heading_to_next(coords, i),
                    "pitch": -45,
                    "duration": 2.0
                })

        # Dairesel tur
        num_circle_points = max(4, config.number_of_points - len(points_to_visit))
        for i in range(num_circle_points):
            angle = (2 * math.pi * i) / num_circle_points
            distance = math.sqrt(parcel.area_m2 / math.pi) * 1.2
            lon = center.x + (distance / 111320) * math.cos(angle)
            lat = center.y + (distance / 111320) * math.sin(angle)

            point = Point(lon, lat)
            if not geometry.contains(point):
                closest_point = geometry.exterior.interpolate(
                    geometry.exterior.project(point)
                )
                lon, lat = closest_point.x, closest_point.y

            points_to_visit.append({
                "lon": lon,
                "lat": lat,
                "height": config.altitude,
                "heading": math.degrees(angle + math.pi / 2),
                "pitch": -30,
                "duration": 1.5
            })

        for point in points_to_visit:
            waypoints.append({
                "longitude": point["lon"],
                "latitude": point["lat"],
                "height": point["height"],
                "heading": point.get("heading", 0),
                "pitch": point.get("pitch", -45),
                "duration": point.get("duration", 1.0),
                "speed": config.speed
            })

        return waypoints, []

    def _calculate_heading(self, lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """İki nokta arası heading hesapla"""
        d_lon = math.radians(lon2 - lon1)
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)

        y = math.sin(d_lon) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(d_lon)

        heading = math.degrees(math.atan2(y, x))
        return (heading + 360) % 360

    def _calculate_heading_to_next(self, coords: List[tuple], current_index: int) -> float:
        """Bir sonraki noktaya doğru heading hesapla"""
        if current_index >= len(coords) - 1:
            return 0

        current = coords[current_index]
        next_point = coords[(current_index + 1) % (len(coords) - 1)]
        return self._calculate_heading(current[0], current[1], next_point[0], next_point[1])

    def _calculate_total_distance(self, waypoints: List[Dict[str, Any]]) -> float:
        """Toplam mesafe hesapla"""
        if len(waypoints) < 2:
            return 0.0

        total = 0.0
        for i in range(len(waypoints) - 1):
            wp1 = waypoints[i]
            wp2 = waypoints[i + 1]

            lat1 = math.radians(wp1["latitude"])
            lon1 = math.radians(wp1["longitude"])
            lat2 = math.radians(wp2["latitude"])
            lon2 = math.radians(wp2["longitude"])

            d_lat = lat2 - lat1
            d_lon = lon2 - lon1

            a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
            c = 2 * math.asin(math.sqrt(a))
            distance = 6371000 * c

            height_diff = abs(wp2.get("height", 0) - wp1.get("height", 0))
            total += math.sqrt(distance ** 2 + height_diff ** 2)

        return total

    def get_drone_tour(self, parcel_id: int) -> Optional[DroneTourResponse]:
        """Kaydedilmiş drone turu varsa al"""
        return None
