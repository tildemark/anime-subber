#!/bin/bash
##############################################
# encode_simple.sh - Simple Video Encoder
# Wrapper script for Linux/macOS
##############################################
#
# This script provides an easy way to run the
# Python video encoder with proper error handling.
#
# USAGE:
#   ./encode_simple.sh input.mp4
#   ./encode_simple.sh input.mp4 output.mkv
#   ./encode_simple.sh "*.mp4"  (batch mode)
#
# FEATURES:
#   - Automatic Python 3 detection
#   - Error handling and user feedback
#   - Supports batch processing with wildcards
#
##############################################

# Set script directory and calculate path to Python scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/encode_simple.py"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.8 or later"
    exit 1
fi

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: encode_simple.py not found at $PYTHON_SCRIPT"
    exit 1
fi

# Display usage if no arguments
if [ $# -eq 0 ]; then
    echo "Usage: ./encode_simple.sh <input_video> [output_mkv]"
    echo "Examples:"
    echo "  ./encode_simple.sh video.mp4"
    echo "  ./encode_simple.sh video.mp4 output.mkv"
    echo "  ./encode_simple.sh \"*.mp4\"  (batch mode)"
    exit 0
fi

# Run the Python script with all arguments passed through
echo "🎬 Starting video encoding..."
python3 "$PYTHON_SCRIPT" "$@"

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Encoding completed successfully!"
else
    echo "❌ Encoding failed. Check the error messages above."
    exit 1
fi
