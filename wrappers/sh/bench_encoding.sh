#!/bin/bash
##############################################
# bench_encoding.sh - Encoding Benchmark Utility
# Wrapper script for Linux/macOS
##############################################
#
# Specialized benchmarking tool for testing
# different encoding parameters and presets.
#
# USAGE:
#   ./bench_encoding.sh input.mp4
#
# FEATURES:
#   - Detailed encoding performance analysis
#   - Tests various preset/CRF combinations
#   - Helps optimize settings
#
##############################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/bench_encoding.py"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: bench_encoding.py not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: ./bench_encoding.sh <input_video>"
    echo "Example: ./bench_encoding.sh sample.mp4"
    exit 0
fi

echo "⏱️  Running encoding benchmark..."
python3 "$PYTHON_SCRIPT" "$@"

if [ $? -eq 0 ]; then
    echo "✅ Encoding benchmark completed!"
else
    echo "❌ Benchmark failed. Check the error messages above."
    exit 1
fi
