#############################################
# bench_encoding.ps1 - Encoding Benchmark Utility
# PowerShell wrapper for Windows
#############################################
#
# Specialized benchmarking tool for testing
# different encoding parameters and presets.
#
# USAGE:
#   .\bench_encoding.ps1 input.mp4
#
# FEATURES:
#   - Detailed encoding performance analysis
#   - Tests various preset/CRF combinations
#
#############################################

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\bench_encoding.py"

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python not found" }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: bench_encoding.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

if ($Arguments.Count -eq 0) {
    Write-Host "Usage: .\bench_encoding.ps1 <input_video>" -ForegroundColor Cyan
    Write-Host "Example: .\bench_encoding.ps1 sample.mp4" -ForegroundColor White
    exit 0
}

Write-Host "⏱️  Running encoding benchmark..." -ForegroundColor Green
& python $PythonScript @Arguments

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Encoding benchmark completed!" -ForegroundColor Green
} else {
    Write-Host "❌ Benchmark failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
