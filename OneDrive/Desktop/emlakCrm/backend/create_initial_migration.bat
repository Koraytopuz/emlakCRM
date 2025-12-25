@echo off
echo ========================================
echo Ilk Migration Olusturuluyor
echo ========================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [HATA] Sanal ortam bulunamadi!
    echo Lutfen once sanal ortami olusturun: python -m venv venv
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [INFO] Alembic versions klasoru olusturuluyor...
if not exist "alembic\versions" (
    mkdir alembic\versions
    echo [OK] Versions klasoru olusturuldu
)

echo.
echo [INFO] Ilk migration olusturuluyor...
alembic revision --autogenerate -m "Initial migration"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Migration olusturuldu!
    echo.
    echo [INFO] Migration'lar calistiriliyor...
    alembic upgrade head
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [OK] Migration'lar basariyla tamamlandi!
        echo Veritabani tablolari olusturuldu.
    ) else (
        echo.
        echo [HATA] Migration calistirilamadi!
    )
) else (
    echo.
    echo [HATA] Migration olusturulamadi!
)

echo.
pause

