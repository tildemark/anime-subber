# ========================================
# AnimeSubber GUI - Installation Test
# ========================================
# This script verifies that all dependencies
# are properly installed for the GUI application.

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AnimeSubber GUI - Installation Test" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$allGood = $true

# ========================================
# Test 1: Python Version
# ========================================
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 8) {
            Write-Host "      ✅ $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host "      ❌ Python 3.8+ required (found: $pythonVersion)" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host "      ❌ Python not found" -ForegroundColor Red
    $allGood = $false
}

# ========================================
# Test 2: FFmpeg
# ========================================
Write-Host "[2/6] Checking FFmpeg..." -ForegroundColor Yellow
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    if ($ffmpegVersion -match "ffmpeg version") {
        Write-Host "      ✅ FFmpeg found" -ForegroundColor Green
    } else {
        Write-Host "      ❌ FFmpeg not found in PATH" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "      ❌ FFmpeg not found in PATH" -ForegroundColor Red
    Write-Host "      ℹ️  You can place ffmpeg.exe in the same folder as main_app.py" -ForegroundColor Gray
    $allGood = $false
}

# ========================================
# Test 3: Gooey
# ========================================
Write-Host "[3/6] Checking Gooey..." -ForegroundColor Yellow
try {
    $gooeyCheck = python -c "import gooey; print(gooey.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✅ Gooey installed (version: $gooeyCheck)" -ForegroundColor Green
    } else {
        Write-Host "      ❌ Gooey not installed" -ForegroundColor Red
        Write-Host "      ℹ️  Run: pip install gooey" -ForegroundColor Gray
        $allGood = $false
    }
} catch {
    Write-Host "      ❌ Gooey not installed" -ForegroundColor Red
    $allGood = $false
}

# ========================================
# Test 4: Whisper CTranslate2
# ========================================
Write-Host "[4/6] Checking whisper-ctranslate2..." -ForegroundColor Yellow
try {
    $whisperCheck = python -c "import whisper_ctranslate2; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✅ whisper-ctranslate2 installed" -ForegroundColor Green
    } else {
        Write-Host "      ❌ whisper-ctranslate2 not installed" -ForegroundColor Red
        Write-Host "      ℹ️  Run: pip install whisper-ctranslate2" -ForegroundColor Gray
        $allGood = $false
    }
} catch {
    Write-Host "      ❌ whisper-ctranslate2 not installed" -ForegroundColor Red
    $allGood = $false
}

# ========================================
# Test 5: PyTorch
# ========================================
Write-Host "[5/6] Checking PyTorch..." -ForegroundColor Yellow
try {
    $torchCheck = python -c "import torch; print(torch.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✅ PyTorch installed (version: $torchCheck)" -ForegroundColor Green
    } else {
        Write-Host "      ❌ PyTorch not installed" -ForegroundColor Red
        Write-Host "      ℹ️  Run: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121" -ForegroundColor Gray
        $allGood = $false
    }
} catch {
    Write-Host "      ❌ PyTorch not installed" -ForegroundColor Red
    $allGood = $false
}

# ========================================
# Test 6: CUDA Availability (Optional)
# ========================================
Write-Host "[6/6] Checking CUDA availability..." -ForegroundColor Yellow
try {
    $cudaCheck = python -c "import torch; print('CUDA' if torch.cuda.is_available() else 'CPU')" 2>&1
    if ($cudaCheck -eq "CUDA") {
        $cudaDevices = python -c "import torch; print(torch.cuda.device_count())" 2>&1
        Write-Host "      ✅ CUDA available ($cudaDevices GPU(s) detected)" -ForegroundColor Green
    } else {
        Write-Host "      ⚠️  CUDA not available (CPU mode only)" -ForegroundColor Yellow
        Write-Host "      ℹ️  Install NVIDIA drivers + CUDA for GPU acceleration" -ForegroundColor Gray
    }
} catch {
    Write-Host "      ⚠️  Could not check CUDA (CPU mode only)" -ForegroundColor Yellow
}

# ========================================
# Test 7: PyInstaller (Optional)
# ========================================
Write-Host "[7/7] Checking PyInstaller (optional)..." -ForegroundColor Yellow
try {
    $pyinstallerCheck = python -c "import PyInstaller; print(PyInstaller.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✅ PyInstaller installed (version: $pyinstallerCheck)" -ForegroundColor Green
    } else {
        Write-Host "      ⚠️  PyInstaller not installed (needed for building .exe)" -ForegroundColor Yellow
        Write-Host "      ℹ️  Run: pip install pyinstaller" -ForegroundColor Gray
    }
} catch {
    Write-Host "      ⚠️  PyInstaller not installed (needed for building .exe)" -ForegroundColor Yellow
}

# ========================================
# Summary
# ========================================
Write-Host "`n========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✅ ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "You're ready to use the GUI application!`n" -ForegroundColor Green
    Write-Host "To launch:" -ForegroundColor White
    Write-Host "  python main_app.py`n" -ForegroundColor Green
} else {
    Write-Host "  ❌ SOME TESTS FAILED" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "Please install missing dependencies:`n" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements_gui.txt`n" -ForegroundColor White
    Write-Host "For FFmpeg installation, see README.md`n" -ForegroundColor White
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
