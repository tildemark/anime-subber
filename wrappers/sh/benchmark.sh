#!/bin/bash
##############################################
# benchmark.sh - Hardware Benchmarking Tool
# Wrapper script for Linux/macOS
##############################################
#
# Tests your hardware's encoding capabilities
# by running 4 preset options and measuring time.
#
# USAGE:
#   ./benchmark.sh input.mp4
#
# FEATURES:
#   - Tests Preset 6, 8, 10, 12
#   - Displays encoding speed for each
#   - Helps choose best settings
#   - Takes ~2 minutes to complete
#
##############################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/benchmark.py"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: benchmark.py not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: ./benchmark.sh <input_video>"
    echo "Example: ./benchmark.sh sample.mp4"
    exit 0
fi

echo "⏱️  Running hardware benchmark..."
python3 "$PYTHON_SCRIPT" "$@"

if [ $? -eq 0 ]; then
    echo "✅ Benchmark completed!"
else
    echo "❌ Benchmark failed. Check the error messages above."
    exit 1
fi
