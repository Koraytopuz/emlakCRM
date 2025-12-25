@echo off
echo Docker ile PostgreSQL baslatiliyor...

REM Docker kontrolu
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo HATA: Docker bulunamadi!
    echo Docker Desktop'i yukleyin: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo Docker bulundu.
echo.

REM Docker Compose ile PostgreSQL'i baslat
echo PostgreSQL container'i baslatiliyor...
cd ..
docker-compose up -d postgres

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo HATA: PostgreSQL baslatilamadi!
    echo Docker Desktop'in calistigindan emin olun.
    pause
    exit /b 1
)

echo.
echo PostgreSQL baslatildi!
echo.

REM .env dosyasi olustur
cd backend
if not exist ".env" (
    echo .env dosyasi olusturuluyor...
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
    echo .env dosyasi olusturuldu!
) else (
    echo .env dosyasi zaten mevcut.
)

echo.
echo PostgreSQL hazir!
echo Backend'i baslatmak icin:
echo   cd backend
echo   .\venv\Scripts\activate.bat
echo   python -m uvicorn main:app --reload
echo.
echo Docker komutlari:
echo   docker-compose ps          - Durumu kontrol et
echo   docker-compose down        - Durdur
echo   docker-compose logs postgres - Loglari goster
echo.
pause

