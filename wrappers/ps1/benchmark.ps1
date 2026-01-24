#############################################
# benchmark.ps1 - Hardware Benchmarking Tool
# PowerShell wrapper for Windows
#############################################
#
# Tests your hardware's encoding capabilities
# by running 4 preset options and measuring time.
#
# USAGE:
#   .\benchmark.ps1 input.mp4
#
# FEATURES:
#   - Tests Preset 6, 8, 10, 12
#   - Displays encoding speed for each
#   - Helps choose best settings
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\benchmark.py"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: benchmark.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\benchmark.ps1 <input_video>" -ForegroundColor Cyan
    Write-Host "Example: .\benchmark.ps1 sample.mp4" -ForegroundColor White
    exit 0
}

Write-Host "⏱️  Running hardware benchmark..." -ForegroundColor Green
& python $PythonScript @Arguments

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Benchmark completed!" -ForegroundColor Green
} else {
    Write-Host "❌ Benchmark failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
