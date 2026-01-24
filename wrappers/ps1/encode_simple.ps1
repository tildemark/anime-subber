#############################################
# encode_simple.ps1 - Simple Video Encoder
# PowerShell wrapper for Windows
#############################################
#
# This script provides an easy way to run the
# Python video encoder from PowerShell.
#
# USAGE:
#   .\encode_simple.ps1 input.mp4
#   .\encode_simple.ps1 input.mp4 output.mkv
#   .\encode_simple.ps1 "*.mp4"  (batch mode)
#
# FEATURES:
#   - Automatic Python 3 detection
#   - Error handling and user feedback
#   - Supports batch processing with wildcards
#   - Works in PowerShell 5.0+
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Get script directory and calculate path to scripts folder
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\encode_simple.py"

# Check if Python 3 is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Run: pip install whisper-ctranslate2" -ForegroundColor Yellow
    exit 1
}

# Check if the Python script exists
if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: encode_simple.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

# Display usage if no arguments
if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\encode_simple.ps1 <input_video> [output_mkv]" -ForegroundColor Cyan
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\encode_simple.ps1 video.mp4" -ForegroundColor White
    Write-Host "  .\encode_simple.ps1 video.mp4 output.mkv" -ForegroundColor White
    Write-Host "  .\encode_simple.ps1 '*.mp4'  (batch mode)" -ForegroundColor White
    exit 0
}

# Run the Python script with all arguments passed through
Write-Host "🎬 Starting video encoding..." -ForegroundColor Green
& python $PythonScript @Arguments

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Encoding completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Encoding failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
