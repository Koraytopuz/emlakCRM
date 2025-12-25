@echo off
echo SQLite kullanimi icin .env dosyasi olusturuluyor...

if exist ".env" (
    echo .env dosyasi mevcut. Uzerine yazmak istiyor musunuz? (E/H)
    set /p overwrite=
    if /i not "%overwrite%"=="E" (
        echo Islem iptal edildi.
        pause
        exit /b 0
    )
)

(
echo # Database Configuration - SQLite
echo DATABASE_URL=sqlite:///./emlakcrm.db
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

echo.
echo .env dosyasi olusturuldu!
echo SQLite veritabani: emlakcrm.db
echo.
echo NOT: SQLite PostGIS desteklemez, cografi ozellikler sinirli olabilir.
echo.
pause

