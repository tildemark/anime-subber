# ========================================
# Quick Setup Script for AnimeSubber GUI
# ========================================
# Run this script to install all dependencies

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AnimeSubber - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Installing dependencies...`n" -ForegroundColor Yellow

# Install from requirements file
pip install -r requirements_gui_pinned.txt

# Force install critical packages that sometimes don't install correctly
Write-Host "`nEnsuring critical packages are installed...`n" -ForegroundColor Yellow
pip install --force-reinstall --no-cache-dir six colored==1.4.4

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "To launch the GUI:" -ForegroundColor Yellow
Write-Host "  python main_app.py`n" -ForegroundColor White

Write-Host "To build .exe:" -ForegroundColor Yellow
Write-Host "  .\build_exe.ps1`n" -ForegroundColor White
