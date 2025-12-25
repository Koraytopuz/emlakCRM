# Veritabanı Kurulum Rehberi

## .env Dosyası Oluşturma

### 1. .env Dosyasını Oluştur

`backend` klasöründe `.env` dosyası oluşturun:

**Windows (PowerShell):**
```powershell
cd backend
Copy-Item .env.example .env
```

**Windows (CMD):**
```cmd
cd backend
copy .env.example .env
```

**Manuel:**
- `backend` klasöründe `.env` adında yeni bir dosya oluşturun
- İçeriğini aşağıdaki gibi doldurun

## PostgreSQL Kurulumu

### Seçenek 1: PostgreSQL Yükleme

1. [PostgreSQL Windows Installer](https://www.postgresql.org/download/windows/) indirin
2. Kurulum sırasında:
   - **Port:** 5432 (varsayılan)
   - **Superuser (postgres) şifresi:** Güçlü bir şifre belirleyin
   - **"Add PostgreSQL to PATH"** seçeneğini işaretleyin
3. Kurulumu tamamlayın

### Seçenek 2: Docker ile PostgreSQL

```cmd
docker-compose up -d
```

Bu komut otomatik olarak PostgreSQL'i başlatır ve veritabanını oluşturur.

## Veritabanı Oluşturma

### PostgreSQL'e Bağlan

**pgAdmin kullanarak:**
1. pgAdmin'i açın
2. Server'a bağlanın (kurulum sırasında belirlediğiniz şifre)
3. Sağ tık → Create → Database
4. Database name: `emlakcrm_db`
5. Owner: `postgres` (veya kendi kullanıcınız)

**Komut satırından:**
```cmd
psql -U postgres
```

PostgreSQL komut satırında:
```sql
CREATE DATABASE emlakcrm_db;
CREATE USER emlakcrm WITH PASSWORD 'emlakcrm123';
GRANT ALL PRIVILEGES ON DATABASE emlakcrm_db TO emlakcrm;
\q
```

### PostGIS Extension Ekle

```sql
psql -U postgres -d emlakcrm_db
```

```sql
CREATE EXTENSION postgis;
\q
```

## .env Dosyasını Düzenle

`.env` dosyasını açın ve `DATABASE_URL`'i düzenleyin:

### Format:
```
DATABASE_URL=postgresql://kullanici_adi:sifre@localhost:5432/veritabani_adi
```

### Örnekler:

**Yeni oluşturduğunuz kullanıcı ile:**
```env
DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db
```

**Postgres superuser ile:**
```env
DATABASE_URL=postgresql://postgres:sizin_sifreniz@localhost:5432/emlakcrm_db
```

**Farklı port kullanıyorsanız:**
```env
DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5433/emlakcrm_db
```

**Uzak sunucu için:**
```env
DATABASE_URL=postgresql://kullanici:sifre@sunucu_ip:5432/emlakcrm_db
```

## Tam .env Örneği

```env
# Database
DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db

# Security
SECRET_KEY=super-secret-key-change-this-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# OpenAI (opsiyonel)
OPENAI_API_KEY=sk-your-openai-api-key-here

# External APIs (opsiyonel)
TKGM_API_URL=
MAPBOX_ACCESS_TOKEN=
```

## Veritabanı Migration'ları Çalıştır

Veritabanı tablolarını oluşturmak için:

```cmd
cd backend
.\venv\Scripts\activate.bat
alembic upgrade head
```

## SQLite Kullanımı (Geçici)

PostgreSQL yüklemeden SQLite ile çalışmak için:

```env
DATABASE_URL=sqlite:///./emlakcrm.db
```

**Not:** SQLite PostGIS desteklemez, bu yüzden coğrafi özellikler çalışmayabilir.

## Bağlantı Testi

Backend'i başlattıktan sonra:

```cmd
curl http://localhost:8000/health
```

Veya tarayıcıda: http://localhost:8000/health

Başarılı ise: `{"status":"healthy"}` döner.

## Sorun Giderme

### "Connection refused" Hatası

- PostgreSQL servisinin çalıştığından emin olun
- Windows Services'te "postgresql-x64-XX" servisinin çalıştığını kontrol edin
- Port 5432'nin açık olduğunu kontrol edin

### "Authentication failed" Hatası

- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- `pg_hba.conf` dosyasını kontrol edin

### "Database does not exist" Hatası

- Veritabanının oluşturulduğundan emin olun
- Veritabanı adının doğru olduğundan emin olun

