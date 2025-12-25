# Sorun Giderme Rehberi

## psycopg2-binary Yükleme Hatası

### Hata Mesajı
```
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

### Çözümler

#### Çözüm 1: PostgreSQL Yükleyin (Önerilen)

1. [PostgreSQL Windows Installer](https://www.postgresql.org/download/windows/) indirin
2. Kurulum sırasında **"Add PostgreSQL to PATH"** seçeneğini işaretleyin
3. Kurulumu tamamlayın
4. Yeni bir terminal açın ve tekrar deneyin:
   ```cmd
   cd backend
   .\start_backend.bat
   ```

#### Çözüm 2: Docker Kullanın (En Kolay)

PostgreSQL yüklemeden Docker ile çalıştırabilirsiniz:

```cmd
docker-compose up -d
```

Bu komut PostgreSQL'i otomatik olarak başlatır.

#### Çözüm 3: Manuel Paket Yükleme

Eğer PostgreSQL yüklemek istemiyorsanız, paketleri manuel olarak yükleyin:

```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install --upgrade pip setuptools wheel
pip install fastapi uvicorn[standard] sqlalchemy alembic pydantic pydantic-settings python-dotenv
pip install geoalchemy2 python-jose[cryptography] passlib[bcrypt] python-multipart requests openai httpx
pip install shapely
```

**Not:** `psycopg2-binary` ve `geopandas` olmadan da backend çalışır, ancak veritabanı bağlantısı olmayacaktır.

## Diğer Yaygın Hatalar

### "uvicorn komutu bulunamadı"

**Çözüm:**
```cmd
cd backend
venv\Scripts\activate.bat
pip install uvicorn[standard]
```

### "Python bulunamadı"

**Çözüm:**
1. Python'un yüklü olduğunu kontrol edin: `python --version`
2. PATH'e eklenmiş mi kontrol edin
3. Yeni bir terminal açın

### Port 8000 Kullanımda

**Çözüm:**
```cmd
# Farklı bir port kullan
uvicorn main:app --reload --port 8001
```

### Veritabanı Bağlantı Hatası

**Çözüm:**
1. PostgreSQL servisinin çalıştığından emin olun
2. `DATABASE_URL` değişkenini kontrol edin
3. Veritabanının oluşturulduğundan emin olun

## Hızlı Test

Backend'in çalışıp çalışmadığını test etmek için:

```cmd
curl http://localhost:8000/health
```

Veya tarayıcıda: http://localhost:8000/health

