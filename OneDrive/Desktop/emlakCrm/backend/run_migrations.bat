@echo off
echo ========================================
echo Veritabani Migration'lari Calistiriliyor
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [HATA] Sanal ortam bulunamadi!
    echo Lutfen once sanal ortami olusturun: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [INFO] Migration durumu kontrol ediliyor...
alembic current

echo.
echo [INFO] Migration'lar calistiriliyor...
alembic upgrade head

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Migration'lar basariyla tamamlandi!
) else (
    echo.
    echo [UYARI] Migration hatasi olabilir.
    echo.
    echo Eger ilk migration yoksa, olusturun:
    echo   alembic revision --autogenerate -m "Initial migration"
    echo   alembic upgrade head
)

echo.
pause

