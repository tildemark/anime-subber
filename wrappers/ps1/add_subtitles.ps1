#############################################
# add_subtitles.ps1 - Subtitle Generator
# PowerShell wrapper for Windows
#############################################
#
# This script adds AI-generated English subtitles
# to existing encoded videos without re-encoding.
#
# USAGE:
#   .\add_subtitles.ps1 input.mkv
#   .\add_subtitles.ps1 input.mkv output.mkv
#   .\add_subtitles.ps1 "*.mp4"  (batch mode)
#
# FEATURES:
#   - Fast: ~30 minutes per video
#   - Uses Whisper AI for translation
#   - Batch processing support
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\add_subtitles.py"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: add_subtitles.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\add_subtitles.ps1 <input_video> [output_mkv]" -ForegroundColor Cyan
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\add_subtitles.ps1 encoded.mkv" -ForegroundColor White
    Write-Host "  .\add_subtitles.ps1 video.mp4 output.mkv" -ForegroundColor White
    Write-Host "  .\add_subtitles.ps1 '*.mp4'  (batch mode)" -ForegroundColor White
    exit 0
}

Write-Host "📝 Starting subtitle generation..." -ForegroundColor Green
& python $PythonScript @Arguments

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Subtitle generation completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Subtitle generation failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
