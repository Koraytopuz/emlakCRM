# Backend Başlatma Rehberi

## Python Yüklü Değilse

1. [Python 3.11+](https://www.python.org/downloads/) indirin ve yükleyin
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
3. Yeni bir terminal açın ve `python --version` komutunu çalıştırın

## Hızlı Başlatma

### Windows

**Yöntem 1: Batch Dosyası (Önerilen)**
```cmd
cd backend
start_backend.bat
```

**Yöntem 2: PowerShell Script**
```powershell
cd backend
.\start_backend.ps1
```

**Not:** PowerShell script çalıştırma hatası alırsanız:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux/macOS

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Manuel Başlatma

1. Backend klasörüne gidin:
   ```bash
   cd backend
   ```

2. Sanal ortam oluşturun:
   ```bash
   python -m venv venv
   ```

3. Sanal ortamı aktif edin:
   - **Windows PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows CMD:**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```

4. Paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

5. Backend'i başlatın:
   ```bash
   uvicorn main:app --reload
   ```

## Sorun Giderme

### "uvicorn komutu bulunamadı" hatası

- Sanal ortamın aktif olduğundan emin olun (terminal'de `(venv)` görünmeli)
- Paketlerin yüklendiğini kontrol edin: `pip list | findstr uvicorn`
- Tekrar yükleyin: `pip install -r requirements.txt`

### "Python bulunamadı" hatası

- Python'un yüklü olduğunu kontrol edin: `python --version`
- PATH'e eklenmiş mi kontrol edin
- `py` komutunu deneyin: `py --version`

### Port 8000 kullanımda

- Başka bir port kullanın: `uvicorn main:app --reload --port 8001`
- Veya 8000 portunu kullanan uygulamayı kapatın

## Backend Çalışıyor mu?

Backend başarıyla çalışıyorsa şu adreslerde erişilebilir olmalı:

- API: http://localhost:8000
- API Dokümantasyonu: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

