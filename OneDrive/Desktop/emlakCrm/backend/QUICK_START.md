# Hızlı Başlatma Rehberi

## Backend Başlatma (Adım Adım)

### 1. Sanal Ortam Oluştur ve Aktif Et

**PowerShell:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Paketleri Yükle

```cmd
pip install --upgrade pip
pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings python-dotenv
pip install geoalchemy2 "python-jose[cryptography]" "passlib[bcrypt]" python-multipart requests openai httpx
pip install shapely
```

### 3. psycopg2-binary Yükle (PostgreSQL için)

**Seçenek A: PostgreSQL Yüklüyse**
```cmd
pip install psycopg2-binary
```

**Seçenek B: PostgreSQL Yüklü Değilse**
- Backend SQLite ile çalışacak (geçici çözüm)
- Veya PostgreSQL yükleyin: https://www.postgresql.org/download/windows/
- Veya Docker kullanın: `docker-compose up -d`

### 4. Backend'i Başlat

```cmd
python -m uvicorn main:app --reload
```

## Hızlı Komutlar

### Tüm Paketleri Yükle
```cmd
pip install -r requirements.txt
```

### Sadece psycopg2-binary Yükle
```cmd
.\install_psycopg2.bat
```

### Otomatik Başlat (Batch)
```cmd
.\start_backend.bat
```

## Sorun Giderme

### "No module named 'psycopg2'" Hatası

**Çözüm 1:** psycopg2-binary yükle
```cmd
pip install psycopg2-binary
```

**Çözüm 2:** SQLite kullan (geçici)
- Backend otomatik olarak SQLite'a geçecek
- Veritabanı: `emlakcrm.db` (backend klasöründe)

**Çözüm 3:** PostgreSQL yükle
- https://www.postgresql.org/download/windows/
- Kurulum sırasında "Add to PATH" seçeneğini işaretle

### Sanal Ortam Aktif Değil

Terminal'de `(venv)` yazısı görünmeli. Görünmüyorsa:

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
venv\Scripts\activate.bat
```

## Backend Çalışıyor mu?

Backend başarıyla çalışıyorsa:

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

