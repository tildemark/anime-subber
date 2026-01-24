#!/bin/bash
##############################################
# add_subtitles.sh - Subtitle Generator
# Wrapper script for Linux/macOS
##############################################
#
# This script adds AI-generated English subtitles
# to existing encoded videos without re-encoding.
#
# USAGE:
#   ./add_subtitles.sh input.mkv
#   ./add_subtitles.sh input.mkv output.mkv
#   ./add_subtitles.sh "*.mp4"  (batch mode)
#
# FEATURES:
#   - Fast: ~30 minutes per video
#   - Uses Whisper AI for translation
#   - Batch processing support
#   - No re-encoding needed
#
##############################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/add_subtitles.py"

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: add_subtitles.py not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Usage: ./add_subtitles.sh <input_video> [output_mkv]"
    echo "Examples:"
    echo "  ./add_subtitles.sh encoded.mkv"
    echo "  ./add_subtitles.sh video.mp4 output.mkv"
    echo "  ./add_subtitles.sh \"*.mp4\"  (batch mode)"
    exit 0
fi

echo "📝 Starting subtitle generation..."
python3 "$PYTHON_SCRIPT" "$@"

if [ $? -eq 0 ]; then
    echo "✅ Subtitle generation completed successfully!"
else
    echo "❌ Subtitle generation failed. Check the error messages above."
    exit 1
fi
