@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Backend Baslatiliyor...
echo ========================================
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
echo [OK] Python bulundu: %PYTHON_CMD%
echo.

REM Sanal ortam kontrolu ve olusturma
if not exist "venv" (
    echo [INFO] Sanal ortam olusturuluyor...
    %PYTHON_CMD% -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [HATA] Sanal ortam olusturulamadi!
        pause
        exit /b 1
    )
    echo [OK] Sanal ortam olusturuldu
) else (
    echo [OK] Sanal ortam mevcut
)
echo.

REM Sanal ortami aktif et
echo [INFO] Sanal ortam aktif ediliyor...
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
    if %ERRORLEVEL% NEQ 0 (
        echo [HATA] Sanal ortam aktif edilemedi!
        pause
        exit /b 1
    )
    echo [OK] Sanal ortam aktif
) else (
    echo [HATA] activate.bat bulunamadi!
    echo Sanal ortam bozuk olabilir. Yeniden olusturuluyor...
    rmdir /s /q venv 2>nul
    %PYTHON_CMD% -m venv venv
    call "venv\Scripts\activate.bat"
)
echo.

REM Paketlerin yuklu olup olmadigini kontrol et
if not exist "venv\Scripts\uvicorn.exe" (
    echo [INFO] Paketler yukleniyor... (Bu biraz zaman alabilir)
    echo.
    
    echo   [1/4] Pip guncelleniyor...
    %PYTHON_CMD% -m pip install --upgrade pip setuptools wheel --quiet
    if %ERRORLEVEL% NEQ 0 (
        echo [UYARI] Pip guncellenemedi, devam ediliyor...
    )
    
    echo   [2/4] Temel paketler yukleniyor...
    pip install fastapi "uvicorn[standard]" sqlalchemy alembic pydantic pydantic-settings python-dotenv
    if %ERRORLEVEL% NEQ 0 (
        echo [HATA] Temel paketler yuklenemedi!
        pause
        exit /b 1
    )
    
    echo   [3/4] PostgreSQL baglayicisi yukleniyor...
    pip install psycopg2-binary
    if %ERRORLEVEL% NEQ 0 (
        echo [UYARI] psycopg2-binary yuklenemedi!
        echo Docker kullaniliyorsa sorun yok, devam ediliyor...
    )
    
    echo   [4/4] Diger paketler yukleniyor...
    pip install geoalchemy2 "python-jose[cryptography]" "passlib[bcrypt]" python-multipart requests openai httpx
    if %ERRORLEVEL% NEQ 0 (
        echo [UYARI] Bazı paketler yuklenemedi, devam ediliyor...
    )
    
    echo   [5/5] Opsiyonel paketler yukleniyor...
    pip install geopandas shapely
    if %ERRORLEVEL% NEQ 0 (
        echo [INFO] Opsiyonel paketler atlandi (geopandas/shapely)
    )
    
    echo.
    echo [OK] Paket yukleme tamamlandi!
) else (
    echo [OK] Paketler zaten yuklu
)
echo.

REM .env dosyasi kontrolu
if not exist ".env" (
    echo [UYARI] .env dosyasi bulunamadi!
    echo Docker kullaniyorsaniz:
    echo   DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db
    echo.
    echo .env dosyasi olusturmak icin: .\create_env.bat
    echo.
)

REM Backend'i baslat
echo ========================================
echo Backend Baslatiliyor...
echo ========================================
echo.
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo Health: http://localhost:8000/health
echo.
echo Durdurmak icin: Ctrl+C
echo.
echo ========================================
echo.

%PYTHON_CMD% -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HATA] Backend baslatilamadi!
    echo.
    echo Sorun giderme:
    echo   1. Sanal ortam aktif mi? (venv) yazisi gorunmeli
    echo   2. Paketler yuklu mu? pip list
    echo   3. Port 8000 acik mi? netstat -ano ^| findstr ":8000"
    echo.
    pause
)

