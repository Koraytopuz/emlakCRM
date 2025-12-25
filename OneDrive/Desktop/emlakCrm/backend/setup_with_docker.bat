@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Docker ile Backend Kurulumu
echo ========================================
echo.

REM Docker kontrolu
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [HATA] Docker bulunamadi!
    echo Docker Desktop'i yukleyin: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo [1/6] Docker kontrol edildi: OK
echo.

REM PostgreSQL'i baslat
echo [2/6] PostgreSQL baslatiliyor...
cd ..
docker-compose up -d postgres

if %ERRORLEVEL% NEQ 0 (
    echo [HATA] PostgreSQL baslatilamadi!
    echo Docker Desktop'in calistigindan emin olun.
    pause
    exit /b 1
)

echo PostgreSQL baslatildi. Biraz bekleniyor...
timeout /t 5 /nobreak >nul

REM PostgreSQL'in hazir olmasini bekle
echo PostgreSQL'in hazir olmasini bekleniyor...
:wait_postgres
docker-compose exec -T postgres pg_isready -U emlakcrm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    timeout /t 2 /nobreak >nul
    goto wait_postgres
)

echo [2/6] PostgreSQL hazir: OK
echo.

cd backend

REM .env dosyasi olustur
echo [3/6] .env dosyasi olusturuluyor...
if not exist ".env" (
    (
    echo # Database Configuration - Docker PostgreSQL
    echo DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db
    echo.
    echo # Security
    echo SECRET_KEY=your-secret-key-change-in-production-use-random-string-here
    echo ALGORITHM=HS256
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30
    echo.
    echo # CORS Origins
    echo CORS_ORIGINS=http://localhost:3000,http://localhost:3001
    echo.
    echo # OpenAI API Key ^(opsiyonel^)
    echo OPENAI_API_KEY=
    echo.
    echo # External APIs ^(opsiyonel^)
    echo TKGM_API_URL=
    echo MAPBOX_ACCESS_TOKEN=
    ) > .env
    echo [3/6] .env dosyasi olusturuldu: OK
) else (
    echo [3/6] .env dosyasi zaten mevcut: OK
)
echo.

REM Python kontrolu
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto :found_python
)

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    goto :found_python
)

where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python3
    goto :found_python
)

echo [HATA] Python bulunamadi!
echo Python yukleyin: https://www.python.org/downloads/
pause
exit /b 1

:found_python
echo [4/6] Python bulundu: %PYTHON_CMD%
echo.

REM Sanal ortam olustur
if not exist "venv" (
    echo [4/6] Sanal ortam olusturuluyor...
    %PYTHON_CMD% -m venv venv
    echo [4/6] Sanal ortam olusturuldu: OK
) else (
    echo [4/6] Sanal ortam zaten mevcut: OK
)
echo.

REM Sanal ortami aktif et
call venv\Scripts\activate.bat

REM Paketleri yukle
if not exist "venv\Scripts\uvicorn.exe" (
    echo [5/6] Paketler yukleniyor... (Bu biraz zaman alabilir)
    echo.
    
    %PYTHON_CMD% -m pip install --upgrade pip setuptools wheel --quiet
    
    echo   - Temel paketler...
    pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings python-dotenv --quiet
    
    echo   - PostgreSQL baglayicisi...
    pip install psycopg2-binary --quiet
    
    echo   - Diger paketler...
    pip install geoalchemy2 "python-jose[cryptography]" "passlib[bcrypt]" python-multipart requests openai httpx --quiet
    
    echo   - Opsiyonel paketler...
    pip install geopandas shapely --quiet 2>nul
    
    echo [5/6] Paketler yuklendi: OK
) else (
    echo [5/6] Paketler zaten yuklu: OK
)
echo.

REM Migration'lari calistir
echo [6/6] Veritabani migration'lari calistiriliyor...
alembic upgrade head

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [UYARI] Migration hatasi olabilir. Devam ediliyor...
) else (
    echo [6/6] Migration'lar tamamlandi: OK
)
echo.

echo ========================================
echo Kurulum Tamamlandi!
echo ========================================
echo.
echo Backend'i baslatmak icin:
echo   .\start_backend.bat
echo.
echo Veya manuel olarak:
echo   venv\Scripts\activate.bat
echo   python -m uvicorn main:app --reload
echo.
echo API Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
pause

