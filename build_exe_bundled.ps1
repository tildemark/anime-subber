# ========================================
# PyInstaller Build Script - BUNDLED VERSION
# ========================================
# This script creates a standalone Windows executable
# WITH bundled FFmpeg and optionally Whisper models.

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AnimeSubber - Build Bundled Executable" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if bundled folder exists
if (-not (Test-Path "bundled")) {
    Write-Host "❌ Bundled folder not found!`n" -ForegroundColor Red
    Write-Host "Please run these scripts first:" -ForegroundColor Yellow
    Write-Host "  1. .\download_ffmpeg.ps1" -ForegroundColor White
    Write-Host "  2. .\download_whisper_models.ps1 (optional)`n" -ForegroundColor White
    exit 1
}

# Check for FFmpeg
if (-not (Test-Path "bundled\ffmpeg.exe")) {
    Write-Host "❌ FFmpeg not found in bundled folder!`n" -ForegroundColor Red
    Write-Host "Please run: .\download_ffmpeg.ps1`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ FFmpeg found in bundled folder" -ForegroundColor Green

# Check for Whisper models (optional)
$bundleModels = $false
if (Test-Path "bundled\whisper-models") {
    Write-Host "✅ Whisper models folder found`n" -ForegroundColor Green
    
    $response = Read-Host "Include Whisper models in .exe? (y/n) [Warning: +500MB]"
    if ($response -eq 'y') {
        $bundleModels = $true
        Write-Host "   Will bundle Whisper models`n" -ForegroundColor Yellow
    } else {
        Write-Host "   Will NOT bundle models (download on first run)`n" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  No Whisper models found (will download on first run)`n" -ForegroundColor Yellow
}

# Check if PyInstaller is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    $null = Get-Command pyinstaller -ErrorAction Stop
    Write-Host "✅ PyInstaller found`n" -ForegroundColor Green
} catch {
    Write-Host "❌ PyInstaller not found. Installing..." -ForegroundColor Red
    pip install pyinstaller
    Write-Host ""
}

# Clean previous builds
if (Test-Path "build") {
    Write-Host "🧹 Cleaning previous build folder..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Write-Host "🧹 Cleaning previous dist folder..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "dist"
}
if (Test-Path "AnimeSubber.spec") {
    Write-Host "🧹 Cleaning previous spec file..." -ForegroundColor Yellow
    Remove-Item -Force "AnimeSubber.spec"
}

Write-Host "`n📦 Building bundled executable..." -ForegroundColor Cyan
Write-Host "   This may take 5-10 minutes...`n" -ForegroundColor Gray

# Build add-data arguments
$addDataArgs = @(
    "--add-data", "bundled\ffmpeg.exe;.",
    "--add-data", "bundled\ffprobe.exe;."
)

if ($bundleModels -and (Test-Path "bundled\whisper-models")) {
    $addDataArgs += "--add-data", "bundled\whisper-models;whisper-models"
}

# Build command
$buildArgs = @(
    "--onefile",
    "--windowed",
    "--name=AnimeSubber",
    "--hidden-import=whisper_ctranslate2",
    "--hidden-import=torch",
    "--hidden-import=gooey",
    "--clean",
    "--noconfirm"
) + $addDataArgs + @("main_app.py")

# Execute PyInstaller
& pyinstaller $buildArgs

# Check if build succeeded
if (Test-Path "dist\AnimeSubber.exe") {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  ✅ BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
    
    $exePath = Resolve-Path "dist\AnimeSubber.exe"
    $exeSize = (Get-Item $exePath).Length / 1MB
    
    Write-Host "📍 Location: $exePath" -ForegroundColor Cyan
    Write-Host "📊 Size: $([math]::Round($exeSize, 2)) MB`n" -ForegroundColor Cyan
    
    Write-Host "📦 Bundled components:" -ForegroundColor Yellow
    Write-Host "   ✅ FFmpeg (included)" -ForegroundColor Green
    Write-Host "   ✅ FFprobe (included)" -ForegroundColor Green
    if ($bundleModels) {
        Write-Host "   ✅ Whisper models (included)" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Whisper models (will download on first run)" -ForegroundColor Yellow
    }
    Write-Host ""
    
    Write-Host "🚀 To run the application:" -ForegroundColor Yellow
    Write-Host "   1. Navigate to: dist\" -ForegroundColor White
    Write-Host "   2. Double-click: AnimeSubber.exe`n" -ForegroundColor White
    
    Write-Host "📝 Distribution notes:" -ForegroundColor Yellow
    Write-Host "   • No FFmpeg installation needed" -ForegroundColor White
    Write-Host "   • No Python installation needed" -ForegroundColor White
    if ($bundleModels) {
        Write-Host "   • Works completely offline" -ForegroundColor White
    } else {
        Write-Host "   • Requires internet for first run (model download)" -ForegroundColor White
    }
    Write-Host "   • CUDA requires NVIDIA drivers installed`n" -ForegroundColor White
    
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "  ❌ BUILD FAILED!" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor Red
    Write-Host "Check the output above for errors.`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
