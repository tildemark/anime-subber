#!/bin/bash
##############################################
# pipeline_windows.sh - Full Pipeline (Windows)
# Wrapper script for Linux/macOS
##############################################
#
# This wrapper exists for consistency but
# pipeline_windows.py is optimized for Windows.
# For best results on Linux/macOS, use:
#   ./pipeline_unix.sh
#
# This script can still run on Unix systems but
# won't have Windows-specific optimizations.
#
# USAGE:
#   ./pipeline_windows.sh input.mp4 [output_mkv]
#   ./pipeline_windows.sh "*.mp4"  (batch mode)
#
##############################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/pipeline_windows.py"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: pipeline_windows.py not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "⚠️  Note: pipeline_windows.py is optimized for Windows."
    echo "   For Linux/macOS, use: ./pipeline_unix.sh"
    echo ""
    echo "Usage: ./pipeline_windows.sh <input_video> [output_mkv]"
    echo "Examples:"
    echo "  ./pipeline_windows.sh movie.mp4"
    echo "  ./pipeline_windows.sh \"*.mp4\"  (batch mode)"
    exit 0
fi

echo "🎬 Starting full pipeline (video encoding + subtitles)..."
python3 "$PYTHON_SCRIPT" "$@"

if [ $? -eq 0 ]; then
    echo "✅ Pipeline completed successfully!"
else
    echo "❌ Pipeline failed. Check the error messages above."
    exit 1
fi
