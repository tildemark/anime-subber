# ========================================
# PyInstaller Build Script - Simple Version
# ========================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AnimeSubber - Build Executable" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check PyInstaller
Write-Host "Checking PyInstaller..." -ForegroundColor Yellow
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $pyinstaller) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }

Write-Host "`nBuilding executable (this may take 5-10 minutes)...`n" -ForegroundColor Cyan

# Build
pyinstaller --onefile --windowed --name=AnimeSubber --hidden-import=whisper_ctranslate2 --hidden-import=torch --hidden-import=gooey --hidden-import=six --clean --noconfirm main_app.py

# Check result
if (Test-Path "dist\AnimeSubber.exe") {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
    
    $size = [math]::Round((Get-Item "dist\AnimeSubber.exe").Length / 1MB, 2)
    Write-Host "Location: dist\AnimeSubber.exe" -ForegroundColor Cyan
    Write-Host "Size: $size MB`n" -ForegroundColor Cyan
    
    Write-Host "IMPORTANT:" -ForegroundColor Yellow
    Write-Host "- FFmpeg must be in PATH or same folder" -ForegroundColor White
    Write-Host "- Whisper models will download on first run (~500 MB)" -ForegroundColor White
    Write-Host "- CUDA requires NVIDIA drivers`n" -ForegroundColor White
} else {
    Write-Host "`nBUILD FAILED! Check errors above.`n" -ForegroundColor Red
    exit 1
}
