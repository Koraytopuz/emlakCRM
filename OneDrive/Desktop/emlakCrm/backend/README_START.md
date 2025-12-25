# Backend Başlatma Rehberi

## Hızlı Başlatma

### Windows CMD (Command Prompt)
```cmd
cd backend
start_backend.bat
```

### Windows PowerShell
```powershell
cd backend
.\start_backend.ps1
```

**Not:** PowerShell'de script çalıştırma hatası alırsanız:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Manuel Başlatma

### 1. Sanal Ortam Oluştur ve Aktif Et

**CMD:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Paketleri Yükle
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Backend'i Başlat

**Önemli:** PowerShell'de `uvicorn` komutu çalışmazsa, Python modülü olarak çalıştırın:

```cmd
python -m uvicorn main:app --reload
```

veya

```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Sorun Giderme

### "uvicorn komutu bulunamadı" Hatası

**Çözüm:** Python modülü olarak çalıştırın:
```cmd
python -m uvicorn main:app --reload
```

### Sanal Ortam Aktif Değil

Sanal ortamın aktif olduğunu görmek için terminal'de `(venv)` yazısı görünmeli.

**CMD'de aktif etme:**
```cmd
venv\Scripts\activate.bat
```

**PowerShell'de aktif etme:**
```powershell
.\venv\Scripts\Activate.ps1
```

### Paketler Yüklenmedi

```cmd
pip install -r requirements.txt
```

Eğer `psycopg2-binary` hatası alırsanız, PostgreSQL yükleyin veya Docker kullanın.

## Backend Çalışıyor mu?

Backend başarıyla çalışıyorsa şu adreslerde erişilebilir olmalı:

- API: http://localhost:8000
- API Dokümantasyonu: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

