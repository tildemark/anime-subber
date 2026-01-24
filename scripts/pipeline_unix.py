"""
===============================================
COMPLETE ANIME PIPELINE - Unix/Linux Version
===============================================
pipeline_unix.py

This is the MAIN all-in-one converter for Linux/macOS that:
1. Converts video to AV1 format (CPU task)
2. Generates AI subtitles via Whisper (GPU task)
3. Muxes subtitles into final MKV file

FULL WORKFLOW: Video → AV1 Encode → AI Translation → Muxing → Final MKV

FEATURES:
  ✓ Works on Linux, macOS, and other Unix-like systems
  ✓ Optional resolution scaling
  ✓ Uses 'nice' command to keep system responsive
  ✓ Generates English subtitles from Japanese audio
  ✓ BATCH: Process multiple videos with wildcard patterns

DEPENDENCIES: ffmpeg, ffprobe, whisper-ctranslate2, 'nice' command

USAGE (Direct Python):
  python pipeline_unix.py <input> [output] [resolution]
  python pipeline_unix.py "*.mp4" [resolution]

USAGE (Shell Wrapper - Recommended):
  ./pipeline_unix.sh input.mp4 output.mkv
  ./pipeline_unix.sh "*.mp4" 1080

EXAMPLES:
  python pipeline_unix.py movie.mp4 out.mkv
  python pipeline_unix.py movie.mp4 out.mkv 1080
  ./pipeline_unix.sh "season1/*.mkv" 1080  (batch mode)
"""

import sys
import subprocess
import os
from glob import glob

# ========== SAFETY CHECK ==========
# This script is Unix-only (uses 'nice' command)
if os.name == 'nt':
    print("❌ Error: This script is optimized for Linux and macOS.")
    print("👉 Please use 'auto_anime_win.py' for Windows systems.")
    sys.exit(1)

# ========== ARGUMENT PARSING ==========
if len(sys.argv) < 2:
    print("Usage: python auto_anime_unix.py <input> [output] [resolution]")
    print("Examples:")
    print("  python auto_anime_unix.py movie.mp4 out.mkv")
    print("  python auto_anime_unix.py movie.mp4 out.mkv 1080")
    print("  python auto_anime_unix.py \"*.mp4\" 1080  (batch mode)")
    sys.exit(1)

input_pattern = sys.argv[1]
output_spec = sys.argv[2] if len(sys.argv) > 2 else None
target_res = sys.argv[3] if len(sys.argv) > 3 else None  # Optional: target resolution

# ========== HELPER FUNCTION ==========
def process_file(input_file, output_file, resolution=None):
    """Process a single video file through the full 3-stage pipeline"""
    input_filename_no_ext = os.path.splitext(os.path.basename(input_file))[0]
    
    # ========== STAGE 1: VIDEO CONVERSION (CPU INTENSIVE) ==========
    print(f"\n{'='*60}")
    print(f"▶️  [1/3] Converting video to AV1...")
    print(f"{'='*60}")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}\n")

    # Build ffmpeg command
    video_cmd = [ffmpeg_path, "-i", input_file]

    # Apply optional resolution scaling
    if resolution:
        video_cmd.extend(["-vf", f"scale=-2:{resolution}:flags=lanczos"])
        print(f"📊 Targeting resolution: {resolution}p\n")

    # Add encoding parameters
    video_cmd.extend([
        "-c:v", "libsvtav1",                   # Video codec: SVT-AV1
        "-preset", "8",                        # Speed preset (8=fastest)
        "-crf", "30",                          # Quality: 0-63 (lower=better)
        "-svtav1-params", "tune=0:enable-overlays=1",
        "-c:a", "libopus",                     # Audio codec: Opus
        "-b:a", "128k",                        # Audio bitrate
        output_file
    ])

    # Execute video encoding at low priority
    subprocess.run(["nice", "-n", "15"] + video_cmd)

    # ========== STAGE 2: AI SUBTITLE GENERATION (GPU/CPU) ==========
    print(f"\n{'='*60}")
    print(f"▶️  [2/3] Generating AI Subtitles (Japanese → English)...")
    print(f"{'='*60}\n")

    input_dir = os.path.dirname(os.path.abspath(input_file))
    srt_file = os.path.join(input_dir, f"{input_filename_no_ext}.srt")

    # Build whisper command
    whisper_cmd = [
        "whisper-ctranslate2",
        input_file,
        "--model", "small",
        "--task", "translate",
        "--language", "ja",
        "--vad_filter", "True",
        "--compute_type", "int8",
        "--output_format", "srt",
        "--output_dir", input_dir
    ]

    # Execute subtitle generation at low priority
    subprocess.run(["nice", "-n", "15"] + whisper_cmd)

    # ========== STAGE 3: MUXING (COMBINING VIDEO + SUBTITLES) ==========
    if os.path.exists(srt_file):
        print(f"\n{'='*60}")
        print(f"▶️  [3/3] Muxing subtitles into final MKV...")
        print(f"{'='*60}\n")
        
        final_output = output_file.replace(".mkv", "_subbed.mkv") if output_file.endswith(".mkv") else output_file + "_subbed.mkv"
        
        # Build muxing command
        mux_cmd = [
            "ffmpeg", 
            "-i", output_file,
            "-i", srt_file,
            "-map", "0", "-map", "1",
            "-c", "copy",
            "-c:s", "srt",
            "-metadata:s:s:0", "language=eng",
            "-metadata:s:s:0", "title=AI English Translation",
            final_output
        ]
        
        subprocess.run(mux_cmd)
        
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS!")
        print(f"{'='*60}")
        print(f"Final subbed file: {final_output}\n")
        return final_output
    else:
        print(f"❌ Error: Could not locate the generated .srt file.")
        return None


ffmpeg_path = "ffmpeg"


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
        output_file = f"{base_name}_av1.mkv"
        
        print(f"\n{'─'*60}")
        print(f"[{i}/{len(files)}] Processing: {input_file}")
        print(f"{'─'*60}")
        
        process_file(input_file, output_file, target_res)
    
    print(f"\n{'='*60}")
    print(f"✅ Batch processing complete! All {len(files)} files processed.")
    print(f"{'='*60}")

else:
    # SINGLE FILE MODE
    input_file = os.path.abspath(files[0])
    
    if output_spec is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_av1.mkv"
    else:
        output_file = os.path.abspath(output_spec)
    
    process_file(input_file, output_file, target_res)
    ]
    
    # Execute muxing (fast, doesn't need low priority)
    subprocess.run(mux_cmd)
    
    print(f"\n✅ Done! Final movie created: {final_output}")
else:
    print(f"\n⚠️  Warning: Subtitle file {srt_file} was not generated.")
    print(f"   Check the output above for Whisper error messages.")