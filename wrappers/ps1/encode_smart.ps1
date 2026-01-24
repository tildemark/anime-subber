#############################################
# encode_smart.ps1 - Smart Video Encoder
# PowerShell wrapper for Windows
#############################################
#
# This script provides an easy way to run the
# smart video encoder with benchmarking.
#
# USAGE:
#   .\encode_smart.ps1 input.mp4
#   .\encode_smart.ps1 input.mp4 output.mkv
#   .\encode_smart.ps1 "*.mp4"  (batch mode)
#
# FEATURES:
#   - Hardware benchmarking (single file mode)
#   - Interactive settings selection
#   - Batch mode uses defaults for speed
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\encode_smart.py"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: encode_smart.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\encode_smart.ps1 <input_video> [output_mkv]" -ForegroundColor Cyan
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\encode_smart.ps1 video.mp4" -ForegroundColor White
    Write-Host "  .\encode_smart.ps1 video.mp4 output.mkv" -ForegroundColor White
    Write-Host "  .\encode_smart.ps1 '*.mkv'  (batch mode)" -ForegroundColor White
    exit 0
}

Write-Host "🎬 Starting smart video encoding..." -ForegroundColor Green
& python $PythonScript @Arguments

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Encoding completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Encoding failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
