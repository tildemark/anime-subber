"""
===================================
VIDEO CONVERTER - Simple AV1 Encoder
===================================
encode_simple.py

SIMPLE video conversion with optional resolution scaling.
- Converts video to AV1 format
- Optional: Downscale to target resolution
- Encodes audio as Opus
- Runs at low priority to keep PC responsive
- BATCH MODE: Supports wildcard patterns (*.mp4, videos/*.mkv)

USAGE (Direct Python):
  python encode_simple.py <input> <output> [resolution]
  python encode_simple.py "*.mp4" [resolution]

USAGE (Wrapper Scripts - Recommended):
  Windows PowerShell: .\encode_simple.ps1 input.mp4
  Linux/macOS:       ./encode_simple.sh input.mp4

EXAMPLES:
  python encode_simple.py input.mp4 output.mkv 720
  .\encode_simple.ps1 input.mp4 output.mkv
  ./encode_simple.sh "season1/*.mp4" 720
"""

import sys
import subprocess
import os
from glob import glob

# ========== HELPER FUNCTION ==========
def convert_single_file(input_file, output_file, target_res):
    """Convert a single video file to AV1"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe") if os.name == 'nt' else "ffmpeg"

    command = [ffmpeg_path, "-i", input_file]

    if target_res:
        command.extend(["-vf", f"scale=-2:{target_res}:flags=lanczos"])
        print(f"📊 Targeting resolution: {target_res}p")
    else:
        print(f"📊 Keeping original size")

    command.extend([
        "-c:v", "libsvtav1",
        "-preset", "8",
        "-crf", "30",
        "-svtav1-params", "tune=0:enable-overlays=1",
        "-c:a", "libopus", "-b:a", "128k",
        output_file
    ])

    print(f"\n🎬 Converting...")
    print(f"   Input:  {input_file}")
    print(f"   Output: {output_file}\n")

    if os.name == 'nt':
        subprocess.run(command, creationflags=0x00004000)
    else:
        subprocess.run(command)


# ========== ARGUMENT VALIDATION ==========
if len(sys.argv) < 2:
    print("Usage: python convert.py <input> [output] [resolution]")
    print("Examples:")
    print("  Single file:  python convert.py input.mp4 output.mkv 720")
    print("  Batch:        python convert.py \"*.mp4\" 720")
    sys.exit(1)

input_pattern = sys.argv[1]
target_res = None
output_file = None

# Parse optional arguments
if len(sys.argv) > 2:
    # Check if it's a resolution number or output file
    if sys.argv[2].isdigit():
        target_res = sys.argv[2]
    else:
        output_file = sys.argv[2]
        if len(sys.argv) > 3 and sys.argv[3].isdigit():
            target_res = sys.argv[3]

# ========== BATCH MODE DETECTION ==========
files = glob(input_pattern)

if not files:
    print(f"❌ No files matched: {input_pattern}")
    sys.exit(1)

if len(files) > 1:
    # BATCH MODE
    print(f"\n{'='*60}")
    print(f"🔄 BATCH MODE - Processing {len(files)} files")
    print(f"{'='*60}\n")
    
    for i, input_file in enumerate(files, 1):
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        out_file = f"{base_name}_encoded.mkv"
        
        print(f"\n[{i}/{len(files)}] Processing: {input_file}")
        convert_single_file(input_file, out_file, target_res)
    
    print(f"\n{'='*60}")
    print(f"✅ Batch conversion complete! All {len(files)} files processed.")
    print(f"{'='*60}")

else:
    # SINGLE FILE MODE
    input_file = files[0]
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_encoded.mkv"
    
    convert_single_file(input_file, output_file, target_res)