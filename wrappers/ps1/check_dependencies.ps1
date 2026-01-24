#############################################
# check_dependencies.ps1 - Dependency Checker
# PowerShell wrapper for Windows
#############################################
#
# This script checks if all required dependencies
# are installed and properly configured.
#
# USAGE:
#   .\check_dependencies.ps1
#
#############################################

# Get script directory and calculate path to scripts folder
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$PythonScript = Join-Path $ProjectRoot "scripts\check_dependencies.py"

# Check if Python 3 is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Error: Python 3 is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if the Python script exists
if (-not (Test-Path $PythonScript)) {
    Write-Host "❌ Error: check_dependencies.py not found at $PythonScript" -ForegroundColor Red
    exit 1
}

# Run the dependency checker
& python $PythonScript
exit $LASTEXITCODE
