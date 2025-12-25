@echo off
setlocal enabledelayedexpansion

echo Backend baslatiliyor...

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

echo Python bulunamadi! Lutfen Python'u yukleyin: https://www.python.org/downloads/
pause
exit /b 1

:found_python
echo Python bulundu: %PYTHON_CMD%

REM Sanal ortam kontrolu ve olusturma
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    %PYTHON_CMD% -m venv venv
)

REM Sanal ortami aktif et
echo Sanal ortam aktif ediliyor...
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
) else (
    echo HATA: Sanal ortam bulunamadi!
    echo Lutfen once sanal ortami olusturun: python -m venv venv
    pause
    exit /b 1
)

REM Paketlerin yuklu olup olmadigini kontrol et
if not exist "venv\Scripts\uvicorn.exe" (
    echo.
    echo Paketler yukleniyor...
    echo.
    echo Pip guncelleniyor...
    %PYTHON_CMD% -m pip install --upgrade pip setuptools wheel
    
    echo.
    echo Temel paketler yukleniyor (1/4)...
    pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings python-dotenv
    if errorlevel 1 (
        echo HATA: Temel paketler yuklenemedi!
        pause
        exit /b 1
    )
    
    echo.
    echo PostgreSQL baglayicisi yukleniyor (2/4)...
    echo NOT: Eger hata alirsaniz, PostgreSQL yuklu olmali veya Docker kullanin.
    pip install psycopg2-binary
    if errorlevel 1 (
        echo.
        echo UYARI: psycopg2-binary yuklenemedi!
        echo Cozum 1: PostgreSQL yukleyin: https://www.postgresql.org/download/windows/
        echo Cozum 2: Docker kullanin: docker-compose up -d
        echo.
        echo Devam ediliyor...
    )
    
    echo.
    echo Diger paketler yukleniyor (3/4)...
    pip install geoalchemy2 "python-jose[cryptography]" "passlib[bcrypt]" python-multipart requests openai httpx
    if errorlevel 1 (
        echo UYARI: Bazı paketler yuklenemedi, devam ediliyor...
    )
    
    echo.
    echo Opsiyonel paketler yukleniyor (4/4)...
    pip install geopandas shapely
    if errorlevel 1 (
        echo Opsiyonel paketler atlandi (geopandas/shapely).
    )
    
    echo.
    echo Paket yukleme tamamlandi!
) else (
    echo Paketler zaten yuklu.
)

REM Backend'i baslat
echo.
echo Backend baslatiliyor...
echo.
echo NOT: Backend http://localhost:8000 adresinde calisacak
echo      Durdurmak icin Ctrl+C basin
echo.
%PYTHON_CMD% -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
