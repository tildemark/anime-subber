#!/bin/bash
##############################################
# check_dependencies.sh - Dependency Checker
# Wrapper script for Linux/macOS
##############################################
#
# This script checks if all required dependencies
# are installed and properly configured.
#
# USAGE:
#   ./check_dependencies.sh
#
##############################################

# Set script directory and calculate path to Python scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/check_dependencies.py"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.8 or later"
    exit 1
fi

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: check_dependencies.py not found at $PYTHON_SCRIPT"
    exit 1
fi

# Run the dependency checker
python3 "$PYTHON_SCRIPT"
exit $?
