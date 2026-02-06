# ========================================
# Download FFmpeg for Bundling
# ========================================
# This script downloads FFmpeg essentials
# for bundling with the application.

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  FFmpeg Download for Bundling" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$downloadPath = ".\ffmpeg-essentials.zip"
$extractPath = ".\ffmpeg-temp"
$targetPath = ".\bundled"

# Create bundled directory
if (-not (Test-Path $targetPath)) {
    New-Item -ItemType Directory -Path $targetPath | Out-Null
}

# Check if already downloaded
if (Test-Path "$targetPath\ffmpeg.exe") {
    Write-Host "✅ FFmpeg already exists in bundled folder" -ForegroundColor Green
    Write-Host "   Location: $targetPath\ffmpeg.exe`n" -ForegroundColor Gray
    
    $response = Read-Host "Re-download? (y/n)"
    if ($response -ne 'y') {
        Write-Host "`nSkipping download.`n" -ForegroundColor Yellow
        exit 0
    }
}

# Download FFmpeg
Write-Host "📥 Downloading FFmpeg essentials..." -ForegroundColor Yellow
Write-Host "   URL: $ffmpegUrl" -ForegroundColor Gray
Write-Host "   Size: ~80 MB (this may take a few minutes)`n" -ForegroundColor Gray

try {
    # Use WebClient for progress
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($ffmpegUrl, $downloadPath)
    Write-Host "✅ Download complete`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Download failed: $_`n" -ForegroundColor Red
    exit 1
}

# Extract archive
Write-Host "📦 Extracting archive..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force
    Write-Host "✅ Extraction complete`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Extraction failed: $_`n" -ForegroundColor Red
    exit 1
}

# Find and copy executables
Write-Host "📋 Copying executables..." -ForegroundColor Yellow

$ffmpegExe = Get-ChildItem -Path $extractPath -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
$ffprobeExe = Get-ChildItem -Path $extractPath -Recurse -Filter "ffprobe.exe" | Select-Object -First 1

if ($ffmpegExe) {
    Copy-Item $ffmpegExe.FullName -Destination "$targetPath\ffmpeg.exe" -Force
    Write-Host "   ✅ ffmpeg.exe copied" -ForegroundColor Green
} else {
    Write-Host "   ❌ ffmpeg.exe not found in archive" -ForegroundColor Red
}

if ($ffprobeExe) {
    Copy-Item $ffprobeExe.FullName -Destination "$targetPath\ffprobe.exe" -Force
    Write-Host "   ✅ ffprobe.exe copied" -ForegroundColor Green
} else {
    Write-Host "   ❌ ffprobe.exe not found in archive" -ForegroundColor Red
}

# Cleanup
Write-Host "`n🧹 Cleaning up..." -ForegroundColor Yellow
Remove-Item $downloadPath -Force
Remove-Item $extractPath -Recurse -Force
Write-Host "✅ Cleanup complete`n" -ForegroundColor Green

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ BUNDLING PREPARATION COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "FFmpeg executables are now in:" -ForegroundColor White
Write-Host "  $targetPath\`n" -ForegroundColor Cyan

$ffmpegSize = (Get-Item "$targetPath\ffmpeg.exe").Length / 1MB
$ffprobeSize = (Get-Item "$targetPath\ffprobe.exe").Length / 1MB

Write-Host "Files:" -ForegroundColor White
Write-Host "  • ffmpeg.exe  ($([math]::Round($ffmpegSize, 2)) MB)" -ForegroundColor Gray
Write-Host "  • ffprobe.exe ($([math]::Round($ffprobeSize, 2)) MB)`n" -ForegroundColor Gray

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Run: .\download_whisper_models.ps1" -ForegroundColor White
Write-Host "  2. Run: .\build_exe_bundled.ps1`n" -ForegroundColor White

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
