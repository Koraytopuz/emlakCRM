from sqlalchemy.orm import Session
from typing import Optional
from openai import OpenAI
from app.core.config import settings
from app.models.listing import Listing
from app.models.parcel import Parcel


class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def generate_listing_description(
        self,
        listing_id: int,
        style: str = "professional",
        language: str = "tr"
    ) -> Optional[str]:
        """AI ile ilan açıklaması oluştur"""
        listing = self.db.query(Listing).filter(Listing.id == listing_id).first()
        if not listing:
            return None
        
        parcel = listing.parcel
        if not parcel:
            return None
        
        # Parsel bilgilerini topla
        parcel_info = {
            "province": parcel.province,
            "district": parcel.district,
            "area": parcel.area_m2,
            "zoning": parcel.zoning_status,
            "price": listing.price
        }
        
        # AI prompt oluştur
        prompt = self._create_prompt(parcel_info, style, language)
        
        try:
            # OpenAI API çağrısı
            if self.client:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Sen profesyonel bir emlak pazarlama uzmanısın."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                description = response.choices[0].message.content
                
                # İlan açıklamasını güncelle
                listing.ai_generated_description = description
                self.db.commit()
                
                return description
            else:
                # API key yoksa örnek metin döndür
                return self._generate_fallback_description(parcel_info, style, language)
        except Exception as e:
            # Hata durumunda fallback
            print(f"OpenAI API error: {e}")
            return self._generate_fallback_description(parcel_info, style, language)

    def _create_prompt(self, parcel_info: dict, style: str, language: str) -> str:
        """AI prompt oluştur"""
        style_map = {
            "professional": "profesyonel ve teknik",
            "casual": "samimi ve anlaşılır",
            "luxury": "lüks ve prestijli"
        }
        
        style_text = style_map.get(style, "profesyonel")
        
        if language == "tr":
            return f"""
            {parcel_info['province']} - {parcel_info['district']} bölgesinde, 
            {parcel_info['area']} m² büyüklüğünde, {parcel_info['zoning']} imar durumlu bir arsa için 
            {style_text} bir emlak ilan açıklaması yaz. Fiyat: {parcel_info['price']} TL.
            """
        else:
            return f"""
            Write a {style_text} real estate listing description for a {parcel_info['area']} m² land 
            in {parcel_info['district']}, {parcel_info['province']} with {parcel_info['zoning']} zoning. 
            Price: {parcel_info['price']} TRY.
            """

    def _generate_fallback_description(self, parcel_info: dict, style: str, language: str) -> str:
        """API olmadan fallback açıklama"""
        if language == "tr":
            return f"""
            {parcel_info['province']} - {parcel_info['district']} bölgesinde konumlanan bu {parcel_info['area']} m² 
            büyüklüğündeki arsa, {parcel_info['zoning']} imar durumu ile yatırım fırsatı sunmaktadır. 
            Detaylı bilgi için iletişime geçiniz.
            """
        else:
            return f"""
            This {parcel_info['area']} m² land located in {parcel_info['district']}, {parcel_info['province']} 
            offers an investment opportunity with {parcel_info['zoning']} zoning status. 
            Contact us for more information.
            """

