@echo off
echo Paketler yukleniyor...

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

echo Python bulunamadi!
pause
exit /b 1

:found_python
echo Python bulundu: %PYTHON_CMD%

REM Sanal ortam kontrolu
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    %PYTHON_CMD% -m venv venv
)

REM Sanal ortami aktif et
call venv\Scripts\activate.bat

REM Pip ve build tools guncelle
echo Pip guncelleniyor...
%PYTHON_CMD% -m pip install --upgrade pip setuptools wheel

REM Temel paketleri once yukle
echo Temel paketler yukleniyor...
pip install fastapi uvicorn[standard] sqlalchemy alembic pydantic pydantic-settings python-dotenv

REM psycopg2-binary'yi ayri yukle (hata olursa devam et)
echo PostgreSQL baglayicisi yukleniyor...
pip install psycopg2-binary --no-cache-dir
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo UYARI: psycopg2-binary yuklenemedi!
    echo PostgreSQL yuklu olmali veya Docker kullanin.
    echo.
)

REM Diger paketleri yukle
echo Diger paketler yukleniyor...
pip install geoalchemy2 python-jose[cryptography] passlib[bcrypt] python-multipart requests openai httpx

REM Opsiyonel paketler (hata olursa devam et)
echo Opsiyonel paketler yukleniyor...
pip install geopandas shapely --no-cache-dir || echo UYARI: geopandas/shapely yuklenemedi (opsiyonel)

echo.
echo Paket yukleme tamamlandi!
echo.
pause

