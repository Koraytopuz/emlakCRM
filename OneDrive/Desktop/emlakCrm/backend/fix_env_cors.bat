@echo off
echo .env dosyasindaki CORS_ORIGINS duzeltiliyor...
echo.

if not exist ".env" (
    echo [HATA] .env dosyasi bulunamadi!
    echo Lutfen once .env dosyasi olusturun: .\create_env.bat
    pause
    exit /b 1
)

REM .env dosyasini yedekle
copy .env .env.backup >nul 2>&1
echo [INFO] .env dosyasi yedeklendi: .env.backup
echo.

REM CORS_ORIGINS satirini bul ve duzelt
findstr /C:"CORS_ORIGINS" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] CORS_ORIGINS bulundu, duzeltiliyor...
    
    REM Gecici dosya olustur
    (
        for /f "tokens=*" %%a in (.env) do (
            set "line=%%a"
            setlocal enabledelayedexpansion
            if "!line:CORS_ORIGINS=!" neq "!line!" (
                echo CORS_ORIGINS=http://localhost:3000,http://localhost:3001
            ) else (
                echo !line!
            )
            endlocal
        )
    ) > .env.tmp
    
    move /y .env.tmp .env >nul
    echo [OK] CORS_ORIGINS duzeltildi
) else (
    echo [INFO] CORS_ORIGINS bulunamadi, ekleniyor...
    echo CORS_ORIGINS=http://localhost:3000,http://localhost:3001 >> .env
    echo [OK] CORS_ORIGINS eklendi
)

echo.
echo .env dosyasi hazir!
echo.
echo NOT: CORS_ORIGINS virgulle ayrilmis format kullanabilir:
echo   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
echo.
pause

