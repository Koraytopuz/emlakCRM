@echo off
echo psycopg2-binary yukleniyor...

REM Sanal ortam kontrolu
if not exist "venv" (
    echo HATA: Sanal ortam bulunamadi!
    echo Once sanal ortam olusturun: python -m venv venv
    pause
    exit /b 1
)

REM Sanal ortami aktif et
call venv\Scripts\activate.bat

echo Pip guncelleniyor...
python -m pip install --upgrade pip setuptools wheel

echo psycopg2-binary yukleniyor...
echo NOT: Eger hata alirsaniz, PostgreSQL yuklu olmali.
python -m pip install psycopg2-binary

if errorlevel 1 (
    echo.
    echo HATA: psycopg2-binary yuklenemedi!
    echo.
    echo Cozumler:
    echo 1. PostgreSQL yukleyin: https://www.postgresql.org/download/windows/
    echo 2. Docker kullanin: docker-compose up -d
    echo 3. SQLite kullanin (gecici): Backend SQLite ile calisacak
    echo.
    pause
) else (
    echo.
    echo Basarili! psycopg2-binary yuklendi.
    echo.
)

pause

