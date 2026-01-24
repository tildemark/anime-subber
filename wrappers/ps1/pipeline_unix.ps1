#############################################
# pipeline_unix.ps1 - Full Pipeline (Linux/macOS)
# PowerShell wrapper (for WSL or PowerShell Core)
#############################################
#
# Complete anime processing pipeline:
#   1. Video encoding (AV1)
#   2. AI subtitle generation
#   3. Muxing into MKV
#
# Note: This script works with PowerShell Core
# on Linux/macOS or WSL on Windows.
#
# USAGE:
#   .\pipeline_unix.ps1 input.mp4
#   .\pipeline_unix.ps1 input.mp4 output.mkv
#   .\pipeline_unix.ps1 "*.mp4" 1080  (batch mode)
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\pipeline_unix.py"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: pipeline_unix.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\pipeline_unix.ps1 <input_video> [output_mkv] [resolution]" -ForegroundColor Cyan
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\pipeline_unix.ps1 movie.mp4" -ForegroundColor White
    Write-Host "  .\pipeline_unix.ps1 movie.mp4 output.mkv" -ForegroundColor White
    Write-Host "  .\pipeline_unix.ps1 movie.mp4 output.mkv 1080" -ForegroundColor White
    Write-Host "  .\pipeline_unix.ps1 '*.mp4' 1080  (batch mode)" -ForegroundColor White
    exit 0
}

Write-Host "🎬 Starting full pipeline (video encoding + subtitles)..." -ForegroundColor Green
& python $PythonScript @Arguments

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Pipeline completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Pipeline failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
