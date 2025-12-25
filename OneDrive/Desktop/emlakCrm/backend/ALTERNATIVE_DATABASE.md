# PostgreSQL Alternatifleri

PostgreSQL kurulumunda sorun yaşıyorsanız, aşağıdaki alternatifleri kullanabilirsiniz:

## 🐳 Seçenek 1: Docker ile PostgreSQL (ÖNERİLEN - En Kolay)

Docker yüklüyse, PostgreSQL'i kurmadan çalıştırabilirsiniz.

### Adımlar:

1. **Docker Desktop'ı başlatın** (yüklü değilse: https://www.docker.com/products/docker-desktop/)

2. **PostgreSQL'i başlatın:**
   ```cmd
   docker-compose up -d postgres
   ```

3. **Veritabanı hazır!** `.env` dosyasını oluşturun:
   ```env
   DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db
   ```

4. **Backend'i başlatın:**
   ```cmd
   cd backend
   .\venv\Scripts\activate.bat
   python -m uvicorn main:app --reload
   ```

**Avantajlar:**
- ✅ Kurulum gerektirmez
- ✅ PostGIS dahil
- ✅ Kolay temizleme: `docker-compose down`

**Docker komutları:**
```cmd
# PostgreSQL'i başlat
docker-compose up -d postgres

# Durumu kontrol et
docker-compose ps

# Durdur
docker-compose down

# Verileri de silmek için
docker-compose down -v
```

---

## 💾 Seçenek 2: SQLite (Hızlı Başlangıç)

PostgreSQL olmadan hızlıca başlamak için SQLite kullanabilirsiniz.

### Adımlar:

1. **`.env` dosyası oluşturun** (veya mevcut olanı düzenleyin):
   ```env
   DATABASE_URL=sqlite:///./emlakcrm.db
   ```

2. **Backend'i başlatın:**
   ```cmd
   cd backend
   .\venv\Scripts\activate.bat
   python -m uvicorn main:app --reload
   ```

**Avantajlar:**
- ✅ Kurulum gerektirmez
- ✅ Hızlı başlangıç
- ✅ Dosya tabanlı (veritabanı `emlakcrm.db` dosyası olarak kaydedilir)

**Dezavantajlar:**
- ❌ PostGIS desteklemez (coğrafi özellikler sınırlı)
- ❌ Production için önerilmez
- ❌ Eşzamanlı kullanıcı desteği sınırlı

**Not:** Backend zaten `psycopg2` yoksa otomatik olarak SQLite'a geçer.

---

## ☁️ Seçenek 3: Cloud PostgreSQL Servisleri (Ücretsiz)

### Supabase (Önerilen)

1. [Supabase](https://supabase.com) hesabı oluşturun (ücretsiz)
2. Yeni proje oluşturun
3. Settings → Database → Connection string'i kopyalayın
4. `.env` dosyasına ekleyin:
   ```env
   DATABASE_URL=postgresql://postgres:[SIFRE]@db.[PROJE-ID].supabase.co:5432/postgres
   ```

**Avantajlar:**
- ✅ Ücretsiz tier mevcut
- ✅ PostGIS dahil
- ✅ Web arayüzü
- ✅ Otomatik yedekleme

### Railway

1. [Railway](https://railway.app) hesabı oluşturun
2. PostgreSQL servisi ekleyin
3. Connection string'i kopyalayın
4. `.env` dosyasına ekleyin

### Neon

1. [Neon](https://neon.tech) hesabı oluşturun
2. Yeni proje oluşturun
3. Connection string'i kopyalayın
4. `.env` dosyasına ekleyin

---

## 🔧 Seçenek 4: Portable PostgreSQL

Kurulum gerektirmeyen portable PostgreSQL:

1. [Portable PostgreSQL](https://www.postgresql.org/download/windows/) indirin
2. ZIP dosyasını çıkarın
3. `bin` klasörünü PATH'e ekleyin
4. `initdb` ve `pg_ctl` komutlarıyla başlatın

---

## 📋 Hızlı Karşılaştırma

| Özellik | Docker | SQLite | Cloud (Supabase) |
|---------|--------|--------|------------------|
| Kurulum | Kolay | Çok Kolay | Kolay |
| PostGIS | ✅ | ❌ | ✅ |
| Ücretsiz | ✅ | ✅ | ✅ (Tier) |
| Production | ✅ | ❌ | ✅ |
| Lokal | ✅ | ✅ | ❌ |

---

## 🚀 Önerilen: Docker

En kolay ve en güçlü çözüm Docker'dır:

```cmd
# 1. Docker Desktop'ı başlatın
# 2. Proje klasöründe:
docker-compose up -d postgres

# 3. Backend'i başlatın
cd backend
.\venv\Scripts\activate.bat
python -m uvicorn main:app --reload
```

**Docker yüklü değilse:** https://www.docker.com/products/docker-desktop/

---

## ❓ Hangi Seçeneği Seçmeliyim?

- **Hızlı test için:** SQLite
- **Geliştirme için:** Docker
- **Production için:** Cloud (Supabase/Railway) veya Docker
- **PostGIS gerekliyse:** Docker veya Cloud

