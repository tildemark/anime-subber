#############################################
# pipeline_windows.ps1 - Full Pipeline (Windows)
# PowerShell wrapper for Windows
#############################################
#
# Complete anime processing pipeline:
#   1. Video encoding (AV1)
#   2. AI subtitle generation
#   3. Muxing into MKV
#
# USAGE:
#   .\pipeline_windows.ps1 input.mp4
#   .\pipeline_windows.ps1 input.mp4 output.mkv
#   .\pipeline_windows.ps1 "*.mp4"  (batch mode)
#
# FEATURES:
#   - Full video + subtitle processing
#   - Batch processing with wildcards
#   - Optional auto-shutdown (add 'y' at end)
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\pipeline_windows.py"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: pipeline_windows.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\pipeline_windows.ps1 <input_video> [output_mkv] [resolution] [preset] [crf] [auto-shutdown]" -ForegroundColor Cyan
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\pipeline_windows.ps1 movie.mp4" -ForegroundColor White
    Write-Host "  .\pipeline_windows.ps1 movie.mp4 output.mkv" -ForegroundColor White
    Write-Host "  .\pipeline_windows.ps1 movie.mp4 output.mkv source 6 30 y" -ForegroundColor White
    Write-Host "  .\pipeline_windows.ps1 '*.mp4'  (batch mode)" -ForegroundColor White
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
