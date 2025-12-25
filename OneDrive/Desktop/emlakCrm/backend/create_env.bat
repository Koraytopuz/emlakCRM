@echo off
echo .env dosyasi olusturuluyor...

if exist ".env" (
    echo .env dosyasi zaten mevcut!
    echo Uzerine yazmak istiyor musunuz? (E/H)
    set /p overwrite=
    if /i not "%overwrite%"=="E" (
        echo Islem iptal edildi.
        pause
        exit /b 0
    )
)

(
echo # Database Configuration
echo # PostgreSQL icin:
echo DATABASE_URL=postgresql://emlakcrm:emlakcrm123@localhost:5432/emlakcrm_db
echo.
echo # Security
echo SECRET_KEY=your-secret-key-change-in-production-use-random-string-here
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo.
echo # CORS Origins ^(virgulle ayrilmis veya JSON formatinda^)
echo CORS_ORIGINS=http://localhost:3000,http://localhost:3001
echo.
echo # OpenAI API Key ^(opsiyonel^)
echo OPENAI_API_KEY=
echo.
echo # External APIs ^(opsiyonel^)
echo TKGM_API_URL=
echo MAPBOX_ACCESS_TOKEN=
) > .env

echo.
echo .env dosyasi olusturuldu!
echo.
echo LUTFEN .env DOSYASINI ACIP DATABASE_URL'I KENDI POSTGRESQL AYARLARINIZA GORE DUZENLEYIN!
echo.
pause

