#!/bin/bash
##############################################
# encode_smart.sh - Smart Video Encoder
# Wrapper script for Linux/macOS
##############################################
#
# This script provides an easy way to run the
# smart video encoder with benchmarking.
#
# USAGE:
#   ./encode_smart.sh input.mp4
#   ./encode_smart.sh input.mp4 output.mkv
#   ./encode_smart.sh "*.mp4"  (batch mode)
#
# FEATURES:
#   - Hardware benchmarking (single file mode)
#   - Interactive settings selection
#   - Batch mode uses defaults for speed
#   - Automatic Python 3 detection
#
##############################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/encode_smart.py"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: encode_smart.py not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: ./encode_smart.sh <input_video> [output_mkv]"
    echo "Examples:"
    echo "  ./encode_smart.sh video.mp4"
    echo "  ./encode_smart.sh video.mp4 output.mkv"
    echo "  ./encode_smart.sh \"*.mkv\"  (batch mode)"
    exit 0
fi

echo "🎬 Starting smart video encoding..."
python3 "$PYTHON_SCRIPT" "$@"

if [ $? -eq 0 ]; then
    echo "✅ Encoding completed successfully!"
else
    echo "❌ Encoding failed. Check the error messages above."
    exit 1
fi
