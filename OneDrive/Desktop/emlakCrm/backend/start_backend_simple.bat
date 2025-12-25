@echo off
echo Backend baslatiliyor...

REM Python kontrolu
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python bulunamadi! Lutfen Python'u yukleyin.
    pause
    exit /b 1
)

echo Python bulundu.

REM Sanal ortam kontrolu
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
)

REM Sanal ortami aktif et
echo Sanal ortam aktif ediliyor...
call venv\Scripts\activate.bat

REM Paketleri yukle
if not exist "venv\Scripts\uvicorn.exe" (
    echo Paketler yukleniyor...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

REM Backend'i baslat
echo Backend baslatiliyor...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

