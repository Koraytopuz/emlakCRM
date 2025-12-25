"""
Test verisi oluşturma script'i
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.parcel import Parcel
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon
import sys

# Tüm modelleri import et
from app.models import *

def create_test_parcels():
    """Test parsel verileri oluştur"""
    db: Session = SessionLocal()
    
    try:
        # Mevcut parsel sayısını kontrol et
        existing_count = db.query(Parcel).count()
        if existing_count > 0:
            print(f"Veritabanında zaten {existing_count} parsel var. Test verisi oluşturulmayacak.")
            return
        
        print("Test parsel verileri oluşturuluyor...")
        
        # Ankara - Çankaya örnek parsel
        ankara_geom = Polygon([
            (32.8597, 39.9334),
            (32.8600, 39.9334),
            (32.8600, 39.9337),
            (32.8597, 39.9337),
            (32.8597, 39.9334)
        ])
        ankara_parcel = Parcel(
            province="Ankara",
            district="Çankaya",
            neighborhood="Kızılay",
            block="123",
            parcel_number="456",
            geometry=from_shape(ankara_geom, srid=4326),
            area_m2=500.0,
            center_lat=39.9334,
            center_lon=32.8597,
            zoning_status="İmar",
            zoning_code="T1",
            source="Test",
            source_id="TEST-001"
        )
        db.add(ankara_parcel)
        
        # İstanbul - Kadıköy örnek parsel
        istanbul_geom = Polygon([
            (29.0233, 40.9833),
            (29.0236, 40.9833),
            (29.0236, 40.9836),
            (29.0233, 40.9836),
            (29.0233, 40.9833)
        ])
        istanbul_parcel = Parcel(
            province="İstanbul",
            district="Kadıköy",
            neighborhood="Moda",
            block="789",
            parcel_number="012",
            geometry=from_shape(istanbul_geom, srid=4326),
            area_m2=750.0,
            center_lat=40.9833,
            center_lon=29.0233,
            zoning_status="İmar",
            zoning_code="T2",
            source="Test",
            source_id="TEST-002"
        )
        db.add(istanbul_parcel)
        
        # İzmir - Konak örnek parsel
        izmir_geom = Polygon([
            (27.1428, 38.4237),
            (27.1431, 38.4237),
            (27.1431, 38.4240),
            (27.1428, 38.4240),
            (27.1428, 38.4237)
        ])
        izmir_parcel = Parcel(
            province="İzmir",
            district="Konak",
            neighborhood="Alsancak",
            block="345",
            parcel_number="678",
            geometry=from_shape(izmir_geom, srid=4326),
            area_m2=600.0,
            center_lat=38.4237,
            center_lon=27.1428,
            zoning_status="İmar",
            zoning_code="T3",
            source="Test",
            source_id="TEST-003"
        )
        db.add(izmir_parcel)
        
        db.commit()
        print("[OK] 3 test parsel basariyla olusturuldu!")
        print("\nOrnek aramalar:")
        print("  - Il: 'Ankara' veya 'Istanbul' veya 'Izmir'")
        print("  - Ilce: 'Cankaya' veya 'Kadikoy' veya 'Konak'")
        print("  - Ada: '123' veya '789' veya '345'")
        print("  - Parsel: '456' veya '012' veya '678'")
        
    except Exception as e:
        db.rollback()
        print(f"[HATA] Hata: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_parcels()

