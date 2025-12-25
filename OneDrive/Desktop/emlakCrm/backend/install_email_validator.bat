@echo off
echo email-validator paketi yukleniyor...
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [HATA] Sanal ortam bulunamadi!
    echo Lutfen once sanal ortami olusturun: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [INFO] email-validator yukleniyor...
pip install email-validator

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] email-validator basariyla yuklendi!
) else (
    echo.
    echo [HATA] email-validator yuklenemedi!
)

echo.
pause

