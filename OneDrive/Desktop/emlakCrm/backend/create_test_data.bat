@echo off
echo ========================================
echo Test Verisi Olusturuluyor
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [HATA] Sanal ortam bulunamadi!
    echo Lutfen once sanal ortami olusturun: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [INFO] Test parsel verileri olusturuluyor...
python create_test_data.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Test verisi basariyla olusturuldu!
) else (
    echo.
    echo [HATA] Test verisi olusturulamadi!
)

echo.
pause

