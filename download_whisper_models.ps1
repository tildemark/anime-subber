# ========================================
# Download Whisper Models for Bundling
# ========================================
# This script downloads Whisper AI models
# for offline bundling with the application.

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Whisper Models Download" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$targetPath = ".\bundled\whisper-models"

# Create models directory
if (-not (Test-Path $targetPath)) {
    New-Item -ItemType Directory -Path $targetPath | Out-Null
}

Write-Host "This script will download Whisper AI models for offline use.`n" -ForegroundColor White

Write-Host "Available models:" -ForegroundColor Yellow
Write-Host "  1. tiny    (~75 MB)   - Fastest, lowest quality" -ForegroundColor Gray
Write-Host "  2. base    (~145 MB)  - Fast, decent quality" -ForegroundColor Gray
Write-Host "  3. small   (~488 MB)  - Balanced (RECOMMENDED)" -ForegroundColor Green
Write-Host "  4. medium  (~1.5 GB)  - Slower, better quality" -ForegroundColor Gray
Write-Host "  5. large   (~3 GB)    - Slowest, best quality`n" -ForegroundColor Gray

Write-Host "Note: The app uses 'small' by default.`n" -ForegroundColor Cyan

$choice = Read-Host "Which model to download? (1-5, or 'all')"

$models = @()
switch ($choice) {
    "1" { $models = @("tiny") }
    "2" { $models = @("base") }
    "3" { $models = @("small") }
    "4" { $models = @("medium") }
    "5" { $models = @("large") }
    "all" { $models = @("tiny", "base", "small", "medium", "large") }
    default {
        Write-Host "`n❌ Invalid choice. Defaulting to 'small'`n" -ForegroundColor Red
        $models = @("small")
    }
}

Write-Host "`n📥 Downloading Whisper models..." -ForegroundColor Yellow
Write-Host "   This will use whisper-ctranslate2 to download models`n" -ForegroundColor Gray

foreach ($model in $models) {
    Write-Host "Downloading model: $model" -ForegroundColor Cyan
    
    try {
        # Use whisper-ctranslate2 to download the model
        # This will cache it in the default location
        python -c "from whisper_ctranslate2 import download_model; download_model('$model')"
        
        Write-Host "✅ Model '$model' downloaded`n" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to download '$model': $_`n" -ForegroundColor Red
    }
}

# Get cache location
Write-Host "`n📍 Finding model cache location..." -ForegroundColor Yellow
try {
    $cacheLocation = python -c "import os; from whisper_ctranslate2 import get_cache_dir; print(get_cache_dir())" 2>$null
    
    if ($cacheLocation) {
        Write-Host "✅ Models cached at:" -ForegroundColor Green
        Write-Host "   $cacheLocation`n" -ForegroundColor Cyan
        
        Write-Host "To bundle models with .exe:" -ForegroundColor Yellow
        Write-Host "  1. Copy models from cache to bundled folder" -ForegroundColor White
        Write-Host "  2. Update PyInstaller spec to include models" -ForegroundColor White
        Write-Host "  3. Set WHISPER_CACHE environment variable in app`n" -ForegroundColor White
    }
} catch {
    Write-Host "⚠️  Could not determine cache location`n" -ForegroundColor Yellow
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ MODEL DOWNLOAD COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Downloaded models: $($models -join ', ')`n" -ForegroundColor White

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Models are cached and ready to use" -ForegroundColor White
Write-Host "  2. Run: .\build_exe_bundled.ps1 (to include in .exe)" -ForegroundColor White
Write-Host "  3. Or just use the app normally`n" -ForegroundColor White

Write-Host "Note: Bundling models in .exe will increase size significantly!" -ForegroundColor Yellow
Write-Host "  • small model: +488 MB" -ForegroundColor Gray
Write-Host "  • Alternative: Download on first run (recommended)`n" -ForegroundColor Gray

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
