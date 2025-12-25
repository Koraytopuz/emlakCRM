# PowerShell Execution Policy Duzeltme Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PowerShell Execution Policy Ayarlaniyor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
Write-Host "Mevcut Execution Policy: $currentPolicy" -ForegroundColor Yellow
Write-Host ""

if ($currentPolicy -eq "Restricted" -or $currentPolicy -eq "AllSigned") {
    Write-Host "Execution policy degistiriliyor..." -ForegroundColor Yellow
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Host "[OK] Execution policy 'RemoteSigned' olarak ayarlandi" -ForegroundColor Green
    } catch {
        Write-Host "[HATA] Execution policy ayarlanamadi!" -ForegroundColor Red
        Write-Host "Manuel olarak calistirin:" -ForegroundColor Yellow
        Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
        pause
        exit 1
    }
} else {
    Write-Host "[OK] Execution policy zaten uygun: $currentPolicy" -ForegroundColor Green
}

Write-Host ""
Write-Host "Artik backend'i baslatabilirsiniz:" -ForegroundColor Green
Write-Host "  .\start_backend.ps1" -ForegroundColor Cyan
Write-Host ""
pause

