#!/bin/bash
##############################################
# pipeline_unix.sh - Full Pipeline (Linux/macOS)
# Wrapper script for Linux/macOS
##############################################
#
# Complete anime processing pipeline:
#   1. Video encoding (AV1)
#   2. AI subtitle generation
#   3. Muxing into MKV
#
# USAGE:
#   ./pipeline_unix.sh input.mp4
#   ./pipeline_unix.sh input.mp4 output.mkv [resolution]
#   ./pipeline_unix.sh "*.mp4" 1080  (batch mode with resolution)
#
# FEATURES:
#   - Full video + subtitle processing
#   - Optional resolution scaling (source, 720, 1080)
#   - Batch processing with wildcards
#   - Uses 'nice' for system responsiveness
#
##############################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/pipeline_unix.py"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: pipeline_unix.py not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: ./pipeline_unix.sh <input_video> [output_mkv] [resolution]"
    echo "Examples:"
    echo "  ./pipeline_unix.sh movie.mp4"
    echo "  ./pipeline_unix.sh movie.mp4 output.mkv"
    echo "  ./pipeline_unix.sh movie.mp4 output.mkv 1080"
    echo "  ./pipeline_unix.sh \"*.mp4\" 1080  (batch mode)"
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
