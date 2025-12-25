from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# Türkiye'deki tüm iller
TURKISH_PROVINCES = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya",
    "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
    "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne",
    "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
    "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars",
    "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya",
    "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas",
    "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van",
    "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman",
    "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye",
    "Düzce"
]

# İl-İlçe eşleştirmeleri (önemli iller için)
PROVINCE_DISTRICTS: Dict[str, List[str]] = {
    "Ankara": ["Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere", "Çankaya", "Çubuk", "Elmadağ", "Güdül", "Haymana", "Kalecik", "Kızılcahamam", "Nallıhan", "Polatlı", "Şereflikoçhisar", "Yenimahalle"],
    "İstanbul": ["Adalar", "Bakırköy", "Beşiktaş", "Beykoz", "Beyoğlu", "Çatalca", "Eyüp", "Fatih", "Gaziosmanpaşa", "Kadıköy", "Kartal", "Sarıyer", "Silivri", "Şile", "Şişli", "Üsküdar", "Zeytinburnu"],
    "İzmir": ["Aliağa", "Bayındır", "Bergama", "Bornova", "Çeşme", "Dikili", "Foça", "Karaburun", "Karşıyaka", "Kemalpaşa", "Kınık", "Kiraz", "Menemen", "Ödemiş", "Seferihisar", "Selçuk", "Tire", "Torbalı", "Urla"],
    "Gaziantep": ["Şahinbey", "Şehitkamil", "Nizip", "İslahiye", "Nurdağı", "Karkamış", "Araban", "Yavuzeli", "Oğuzeli"],
    "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "Mudanya", "Gemlik", "İnegöl", "Mustafakemalpaşa", "Orhangazi", "Karacabey"],
    "Antalya": ["Muratpaşa", "Kepez", "Konyaaltı", "Alanya", "Manavgat", "Kaş", "Kemer", "Serik"],
    "Kocaeli": ["İzmit", "Gebze", "Körfez", "Gölcük", "Derince", "Karamürsel", "Kandıra"],
    "Adana": ["Seyhan", "Yüreğir", "Çukurova", "Sarıçam", "Ceyhan", "Kozan", "İmamoğlu"],
    "Konya": ["Selçuklu", "Karatay", "Meram", "Akşehir", "Beyşehir", "Ereğli", "Karapınar"],
    "Mersin": ["Akdeniz", "Mezitli", "Toroslar", "Yenişehir", "Tarsus", "Erdemli", "Silifke"],
}

@router.get("/provinces", response_model=List[str])
async def get_provinces():
    """Türkiye'deki tüm illeri döndür (alfabetik sıralı)"""
    # Türkçe karakterler için doğru sıralama
    return sorted(TURKISH_PROVINCES, key=lambda x: x.lower())

@router.get("/districts/{province}", response_model=List[str])
async def get_districts(province: str):
    """Belirtilen ile ait ilçeleri döndür"""
    import logging
    import sys
    import urllib.parse
    
    # URL decode yap (eğer encode edilmişse)
    province_decoded = urllib.parse.unquote(province)
    # İl adını normalize et (büyük/küçük harf duyarsız, başında/sonunda boşlukları temizle)
    province_normalized = province_decoded.strip()
    
    print(f"[DEBUG] İlçe isteği alındı - Orijinal: '{province}', Decoded: '{province_decoded}', Normalized: '{province_normalized}'", file=sys.stderr)
    
    # Özel durumlar: "İçel (Mersin)" -> "Mersin" eşleştirmesi
    province_mapping = {
        "mersin": "Mersin",
        "içel": "Mersin",
        "içel (mersin)": "Mersin",
    }
    
    # Mapping kontrolü
    province_lower = province_normalized.lower()
    if province_lower in province_mapping:
        province_normalized = province_mapping[province_lower]
        print(f"[DEBUG] İl adı mapping ile değiştirildi: '{province_normalized}'", file=sys.stderr)
    
    # Tam eşleşme ara (case-insensitive, Türkçe karakterler için)
    for prov, districts in PROVINCE_DISTRICTS.items():
        # Türkçe karakterleri normalize et
        prov_normalized = prov.strip().lower()
        province_lower_check = province_normalized.lower()
        
        print(f"[DEBUG] Karşılaştırma - Backend: '{prov}' ({prov_normalized}) vs Frontend: '{province_normalized}' ({province_lower_check})", file=sys.stderr)
        
        if prov_normalized == province_lower_check:
            sorted_districts = sorted(districts, key=lambda x: x.lower())
            print(f"[DEBUG] ✅ İlçeler bulundu - İl: '{prov}', İlçe sayısı: {len(sorted_districts)}", file=sys.stderr)
            print(f"[DEBUG] İlçeler: {sorted_districts}", file=sys.stderr)
            return sorted_districts
    
    # Eğer ilçe listesi yoksa, boş liste döndür
    print(f"[DEBUG] ❌ İlçe bulunamadı - İl: '{province_normalized}'", file=sys.stderr)
    print(f"[DEBUG] Mevcut iller: {list(PROVINCE_DISTRICTS.keys())}", file=sys.stderr)
    return []

