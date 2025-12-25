from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.shape import from_shape
from shapely.geometry import shape, mapping
from typing import List, Optional

from app.models.parcel import Parcel
from app.schemas.parcel import ParcelCreate, ParcelSearch


class ParcelService:
    def __init__(self, db: Session):
        self.db = db

    def search_parcels(self, search: ParcelSearch) -> List[Parcel]:
        """Parsel sorgulama"""
        import sys
        
        query = self.db.query(Parcel)
        
        print(f"[DEBUG ParcelService] Arama parametreleri: province={search.province}, district={search.district}, block={search.block}, parcel_number={search.parcel_number}", file=sys.stderr)
        
        if search.province:
            query = query.filter(Parcel.province.ilike(f"%{search.province}%"))
            print(f"[DEBUG ParcelService] İl filtresi eklendi: {search.province}", file=sys.stderr)
        if search.district:
            query = query.filter(Parcel.district.ilike(f"%{search.district}%"))
            print(f"[DEBUG ParcelService] İlçe filtresi eklendi: {search.district}", file=sys.stderr)
        if search.block:
            # Block'u string olarak karşılaştır (veritabanında string olarak saklanıyor)
            block_str = str(search.block).strip()
            print(f"[DEBUG ParcelService] Ada filtresi eklendi: '{block_str}' (type: {type(search.block)})", file=sys.stderr)
            # String karşılaştırması yap
            query = query.filter(Parcel.block == block_str)
        if search.parcel_number:
            # Parcel_number'ı string olarak karşılaştır
            parcel_str = str(search.parcel_number).strip()
            print(f"[DEBUG ParcelService] Parsel filtresi eklendi: '{parcel_str}' (type: {type(search.parcel_number)})", file=sys.stderr)
            # String karşılaştırması yap
            query = query.filter(Parcel.parcel_number == parcel_str)
        
        # SQL sorgusunu logla
        print(f"[DEBUG ParcelService] SQL sorgusu hazırlandı", file=sys.stderr)
        results = query.all()
        print(f"[DEBUG ParcelService] Bulunan parsel sayısı: {len(results)}", file=sys.stderr)
        
        # Bulunan parselleri logla
        for i, parcel in enumerate(results):
            print(f"[DEBUG ParcelService] Parsel {i+1}: ID={parcel.id}, İl={parcel.province}, İlçe={parcel.district}, Ada={parcel.block}, Parsel={parcel.parcel_number}", file=sys.stderr)
        
        return results

    def get_parcel_by_id(self, parcel_id: int) -> Optional[Parcel]:
        return self.db.query(Parcel).filter(Parcel.id == parcel_id).first()

    def create_parcel(self, parcel_data: ParcelCreate) -> Parcel:
        """Yeni parsel oluştur"""
        # GeoJSON'dan PostGIS geometry'ye dönüştür
        geom = shape(parcel_data.geometry)
        geometry = from_shape(geom, srid=4326)
        
        db_parcel = Parcel(
            province=parcel_data.province,
            district=parcel_data.district,
            neighborhood=parcel_data.neighborhood,
            block=parcel_data.block,
            parcel_number=parcel_data.parcel_number,
            geometry=geometry,
            area_m2=parcel_data.area_m2,
            center_lat=parcel_data.center_lat,
            center_lon=parcel_data.center_lon,
            zoning_status=parcel_data.zoning_status,
            zoning_code=parcel_data.zoning_code,
            source=parcel_data.source,
            source_id=parcel_data.source_id
        )
        self.db.add(db_parcel)
        self.db.commit()
        self.db.refresh(db_parcel)
        return db_parcel

    def get_parcel_geometry(self, parcel_id: int, format: str = "geojson") -> dict:
        """Parsel geometrisini al"""
        parcel = self.get_parcel_by_id(parcel_id)
        if not parcel:
            return None
        
        # PostGIS geometry'den GeoJSON'a dönüştür
        geom = parcel.geometry
        shapely_geom = geom.__geo_interface__
        
        if format == "geojson":
            return {
                "type": "Feature",
                "geometry": shapely_geom,
                "properties": {
                    "id": parcel.id,
                    "parcel_number": parcel.parcel_number
                }
            }
        elif format == "wkt":
            return {"wkt": geom.wkt}
        
        return None

