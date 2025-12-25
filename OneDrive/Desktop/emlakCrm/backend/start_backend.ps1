# PowerShell script for starting backend
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend Baslatiliyor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Python kontrolu
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "[HATA] Python bulunamadi!" -ForegroundColor Red
    Write-Host "Python yukleyin: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[OK] Python bulundu: $pythonCmd" -ForegroundColor Green
Write-Host ""

# Sanal ortam kontrolu
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Sanal ortam olusturuluyor..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[HATA] Sanal ortam olusturulamadi!" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "[OK] Sanal ortam olusturuldu" -ForegroundColor Green
} else {
    Write-Host "[OK] Sanal ortam mevcut" -ForegroundColor Green
}
Write-Host ""

# Sanal ortami aktif et
Write-Host "[INFO] Sanal ortam aktif ediliyor..." -ForegroundColor Yellow

# Execution policy kontrolu ve ayarlama
$executionPolicy = Get-ExecutionPolicy -Scope CurrentUser
if ($executionPolicy -eq "Restricted" -or $executionPolicy -eq "AllSigned") {
    Write-Host "[INFO] Execution policy ayarlaniyor..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force -ErrorAction Stop
        Write-Host "[OK] Execution policy ayarlandi" -ForegroundColor Green
    } catch {
        Write-Host "[UYARI] Execution policy ayarlanamadi, alternatif yontem kullaniliyor..." -ForegroundColor Yellow
    }
}

# Activate.ps1 yerine doğrudan Python'u venv'den çağır (daha güvenilir)
if (Test-Path "venv\Scripts\python.exe") {
    $venvPython = Resolve-Path "venv\Scripts\python.exe"
    $env:VIRTUAL_ENV = (Resolve-Path "venv").Path
    $env:PATH = "$((Resolve-Path "venv\Scripts").Path);$env:PATH"
    Write-Host "[OK] Sanal ortam aktif (venv Python kullaniliyor)" -ForegroundColor Green
    # Python komutunu venv'den kullan
    $pythonCmd = $venvPython
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    try {
        & .\venv\Scripts\Activate.ps1
        Write-Host "[OK] Sanal ortam aktif" -ForegroundColor Green
    } catch {
        Write-Host "[UYARI] Activate.ps1 calistirilamadi, venv Python dogrudan kullaniliyor..." -ForegroundColor Yellow
        $venvPython = Resolve-Path "venv\Scripts\python.exe"
        $env:VIRTUAL_ENV = (Resolve-Path "venv").Path
        $env:PATH = "$((Resolve-Path "venv\Scripts").Path);$env:PATH"
        $pythonCmd = $venvPython
    }
} else {
    Write-Host "[HATA] Sanal ortam script'leri bulunamadi!" -ForegroundColor Red
    Write-Host "Sanal ortam bozuk olabilir. Yeniden olusturuluyor..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
    & $pythonCmd -m venv venv
    if (Test-Path "venv\Scripts\python.exe") {
        $venvPython = Resolve-Path "venv\Scripts\python.exe"
        $env:VIRTUAL_ENV = (Resolve-Path "venv").Path
        $env:PATH = "$((Resolve-Path "venv\Scripts").Path);$env:PATH"
        $pythonCmd = $venvPython
        Write-Host "[OK] Sanal ortam yeniden olusturuldu ve aktif" -ForegroundColor Green
    } else {
        Write-Host "[HATA] Sanal ortam olusturulamadi!" -ForegroundColor Red
        pause
        exit 1
    }
}
Write-Host ""

# Paketleri yukle
if (-not (Test-Path "venv\Scripts\uvicorn.exe")) {
    Write-Host "[INFO] Paketler yukleniyor... (Bu biraz zaman alabilir)" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "  [1/4] Pip guncelleniyor..." -ForegroundColor Cyan
    & "$pythonCmd" -m pip install --upgrade pip setuptools wheel --quiet
    
    Write-Host "  [2/4] Temel paketler yukleniyor..." -ForegroundColor Cyan
    & "$pythonCmd" -m pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings python-dotenv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[HATA] Temel paketler yuklenemedi!" -ForegroundColor Red
        pause
        exit 1
    }
    
    Write-Host "  [3/4] PostgreSQL baglayicisi yukleniyor..." -ForegroundColor Cyan
    & "$pythonCmd" -m pip install psycopg2-binary
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[UYARI] psycopg2-binary yuklenemedi!" -ForegroundColor Yellow
        Write-Host "Docker kullaniliyorsa sorun yok, devam ediliyor..." -ForegroundColor Yellow
    }
    
    Write-Host "  [4/4] Diger paketler yukleniyor..." -ForegroundColor Cyan
    & "$pythonCmd" -m pip install geoalchemy2 "python-jose[cryptography]" "passlib[bcrypt]" python-multipart requests openai httpx
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[UYARI] Bazı paketler yuklenemedi, devam ediliyor..." -ForegroundColor Yellow
    }
    
    Write-Host "  [5/5] Opsiyonel paketler yukleniyor..." -ForegroundColor Cyan
    & "$pythonCmd" -m pip install geopandas shapely
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[INFO] Opsiyonel paketler atlandi (geopandas/shapely)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "[OK] Paket yukleme tamamlandi!" -ForegroundColor Green
} else {
    Write-Host "[OK] Paketler zaten yuklu" -ForegroundColor Green
}
Write-Host ""

# .env dosyasi kontrolu
if (-not (Test-Path ".env")) {
    Write-Host "[UYARI] .env dosyasi bulunamadi!" -ForegroundColor Yellow
    Write-Host "Docker kullaniyorsaniz:" -ForegroundColor Yellow
    Write-Host "  DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db" -ForegroundColor Cyan
    Write-Host ""
    Write-Host ".env dosyasi olusturmak icin: .\create_env.bat" -ForegroundColor Yellow
    Write-Host ""
}

# Backend'i baslat
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend Baslatiliyor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API: http://localhost:8000" -ForegroundColor Green
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Health: http://localhost:8000/health" -ForegroundColor Green
Write-Host ""
Write-Host "Durdurmak icin: Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& "$pythonCmd" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[HATA] Backend baslatilamadi!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Sorun giderme:" -ForegroundColor Yellow
    Write-Host "  1. Sanal ortam aktif mi? (venv) yazisi gorunmeli" -ForegroundColor White
    Write-Host "  2. Paketler yuklu mu? pip list" -ForegroundColor White
    Write-Host "  3. Port 8000 acik mi? netstat -ano | findstr ':8000'" -ForegroundColor White
    Write-Host ""
    pause
}
