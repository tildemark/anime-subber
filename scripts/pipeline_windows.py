"""
===============================================
COMPLETE ANIME PIPELINE - Windows Version
===============================================
pipeline_windows.py

This is the MAIN all-in-one converter that:
1. Converts video to AV1 format (CPU task)
2. Generates AI subtitles via Whisper (GPU task)
3. Muxes subtitles into final MKV file

FULL WORKFLOW: Video → AV1 Encode → AI Translation → Muxing → Final MKV

FEATURES:
  ✓ Configurable resolution, preset, and CRF via command line
  ✓ Supports optional PC shutdown when done
  ✓ Uses low priority to keep PC responsive
  ✓ Generates English subtitles from Japanese audio
  ✓ BATCH MODE: Supports wildcard patterns (*.mp4, videos/*.mkv)

DEPENDENCIES: ffmpeg, whisper-ctranslate2

USAGE (Direct Python):
  python pipeline_windows.py <input> <output> [res] [preset] [crf] [shutdown]
  python pipeline_windows.py "*.mp4" [res] [preset] [crf]

USAGE (PowerShell Wrapper - Recommended):
  .\pipeline_windows.ps1 input.mp4 output.mkv
  .\pipeline_windows.ps1 "*.mp4"

EXAMPLES:
  python pipeline_windows.py movie.mp4 out.mkv
  python pipeline_windows.py movie.mp4 out.mkv source 8 30
  python pipeline_windows.py movie.mp4 out.mkv 720 10 40 y
  python pipeline_windows.py "*.mp4"
  .\pipeline_windows.ps1 "season1/*.mkv" source 6 30
"""

import sys
import subprocess
import os
from glob import glob

# ========== SAFETY CHECK ==========
# This script is Windows-only (uses creationflags)
if os.name != 'nt':
    print("❌ Error: This script is for Windows. Use auto_anime_unix.py for Linux/macOS.")
    sys.exit(1)

# ========== DEFAULT SETTINGS ==========
# Customize these if you have different preferences
DEFAULT_RES = "source"      # "source" or "720" or "1080" etc.
DEFAULT_PRESET = "6"        # 0-10 (lower=better quality, slower)
DEFAULT_CRF = "30"          # 0-63 (lower=better quality)
DEFAULT_SHUTDOWN = "n"      # "y" or "n"

# ========== ARGUMENT PARSING ==========
if len(sys.argv) < 2:
    print("\n" + "="*50)
    print("  ANIME AV1 SUBBER (Windows)")
    print("="*50)
    print("\nUsage: python auto_anime_win.py <input> [output] [res] [preset] [crf] [shutdown]")
    print("Examples:")
    print("  python auto_anime_win.py in.mp4 out.mkv")
    print("  python auto_anime_win.py in.mp4 out.mkv source 8 30 y")
    print("  python auto_anime_win.py \"*.mp4\"  (batch mode)")
    sys.exit(1)

input_pattern = sys.argv[1]
output_spec = sys.argv[2] if len(sys.argv) > 2 else None
res = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_RES
preset = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_PRESET
crf = sys.argv[5] if len(sys.argv) > 5 else DEFAULT_CRF
halt = sys.argv[6].lower() if len(sys.argv) > 6 else DEFAULT_SHUTDOWN

# ========== HELPER FUNCTION ==========
def process_file(input_vid, output_vid, res, preset, crf, halt):
    """Process a single video file through the full pipeline"""
    LOW_PRIORITY = 0x00004000
    ffmpeg_path = "ffmpeg"

    # ========== STAGE 1: VIDEO CONVERSION (CPU INTENSIVE) ==========
    print("\n" + "="*60)
    print("▶️  [1/3] Converting video to AV1 codec...")
    print("="*60)
    print(f"Input:  {input_vid}")
    print(f"Output: {output_vid}")
    print(f"Settings: Resolution={res}, Preset={preset}, CRF={crf}\n")

    scale = f"scale=-2:{res}:flags=lanczos" if res != "source" else "null"

    video_cmd = [
        ffmpeg_path, "-i", input_vid,
        "-vf", scale,
        "-c:v", "libsvtav1", 
        "-preset", preset, 
        "-crf", crf,
        "-svtav1-params", "tune=0:enable-overlays=1:lookahead=120",
        "-c:a", "libopus", 
        "-b:a", "128k",
        output_vid
    ]

    subprocess.run(video_cmd, creationflags=LOW_PRIORITY)

    # ========== STAGE 2: AI TRANSLATION (GPU INTENSIVE) ==========
    print("\n" + "="*60)
    print("▶️  [2/3] Generating AI Subtitles (Japanese → English)...")
    print("="*60 + "\n")

    srt_file = os.path.splitext(input_vid)[0] + ".srt"

    whisper_cmd = [
        "whisper-ctranslate2",
        input_vid,
        "--model", "small",
        "--task", "translate",
        "--language", "ja",
        "--vad_filter", "True",
        "--compute_type", "int8",
        "--output_format", "srt",
        "--output_dir", os.path.dirname(os.path.abspath(input_vid))
    ]

    subprocess.run(whisper_cmd, creationflags=LOW_PRIORITY)

    # ========== STAGE 3: MUXING (FAST) ==========
    if os.path.exists(srt_file):
        print("\n" + "="*60)
        print("▶️  [3/3] Muxing subtitles into final MKV...")
        print("="*60 + "\n")
        
        final_output = output_vid.replace(".mkv", "_final.mkv")
        
        mux_cmd = [
            ffmpeg_path, "-i", output_vid, "-i", srt_file,
            "-map", "0", "-map", "1",
            "-c", "copy",
            "-c:s", "srt",
            "-metadata:s:s:0", "language=eng",
            "-metadata:s:s:0", "title=AI English Translation",
            final_output
        ]
        
        subprocess.run(mux_cmd)
        print(f"\n✅ Success! Final file: {final_output}")
        return final_output
    else:
        print("\n⚠️  Warning: Subtitle file not found. Whisper step may have failed.")
        return None


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
    print(f"Settings: Resolution={res}, Preset={preset}, CRF={crf}\n")
    
    for i, input_file in enumerate(files, 1):
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_encoded.mkv"
        
        print(f"\n{'─'*60}")
        print(f"[{i}/{len(files)}] Processing: {input_file}")
        print(f"{'─'*60}")
        
        process_file(input_file, output_file, res, preset, crf, "n")
    
    print(f"\n{'='*60}")
    print(f"✅ Batch conversion complete! All {len(files)} files processed.")
    print(f"{'='*60}")

else:
    # SINGLE FILE MODE
    input_vid = files[0]
    
    if output_spec is None:
        base_name = os.path.splitext(os.path.basename(input_vid))[0]
        output_vid = f"{base_name}_encoded.mkv"
    else:
        output_vid = output_spec
    
    final_file = process_file(input_vid, output_vid, res, preset, crf, halt)
    
    # ========== OPTIONAL: SHUTDOWN PC ==========
    if halt == 'y' and final_file:
        print("\n⏻️  System shutting down in 60 seconds...")
        os.system("shutdown /s /t 60")
    print("\nUsage: python auto_anime_win.py <input> <output> [res] [preset] [crf] [shutdown]")
    print(f"\nDefaults: {DEFAULT_RES} | Preset {DEFAULT_PRESET} | CRF {DEFAULT_CRF}")
    print("\nExamples:")
    print("  python auto_anime_win.py in.mp4 out.mkv")
    print("  python auto_anime_win.py in.mp4 out.mkv 720 8 30")
    print("  python auto_anime_win.py in.mp4 out.mkv source 6 30 y")
    sys.exit(1)

# Get arguments with fallback to defaults
input_vid = sys.argv[1]
output_vid = sys.argv[2]
res     = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_RES
preset  = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_PRESET
crf     = sys.argv[5] if len(sys.argv) > 5 else DEFAULT_CRF
halt    = sys.argv[6].lower() if len(sys.argv) > 6 else DEFAULT_SHUTDOWN

LOW_PRIORITY = 0x00004000  # Windows: BELOW_NORMAL_PRIORITY_CLASS
ffmpeg_path = "ffmpeg"

# ========== STAGE 1: VIDEO CONVERSION (CPU INTENSIVE) ==========
print("\n" + "="*60)
print("▶️  [1/3] Converting video to AV1 codec...")
print("="*60)
print(f"Input:  {input_vid}")
print(f"Output: {output_vid}")
print(f"Settings: Resolution={res}, Preset={preset}, CRF={crf}\n")

# Build scaling filter
scale = f"scale=-2:{res}:flags=lanczos" if res != "source" else "null"

# Build ffmpeg command
video_cmd = [
    ffmpeg_path, "-i", input_vid,
    "-vf", scale,
    "-c:v", "libsvtav1", 
    "-preset", preset, 
    "-crf", crf,
    "-svtav1-params", "tune=0:enable-overlays=1:lookahead=120",  # Anime tuning
    "-c:a", "libopus", 
    "-b:a", "128k",
    output_vid
]

# Execute video encoding (runs at low priority to keep PC responsive)
subprocess.run(video_cmd, creationflags=LOW_PRIORITY)

# ========== STAGE 2: AI TRANSLATION (GPU INTENSIVE) ==========
print("\n" + "="*60)
print("▶️  [2/3] Generating AI Subtitles (Japanese → English)...")
print("="*60 + "\n")

# Determine where SRT file will be created
srt_file = os.path.splitext(input_vid)[0] + ".srt"

# Build whisper command
whisper_cmd = [
    "whisper-ctranslate2",
    input_vid,
    "--model", "small",              # "tiny", "small", "base", "medium", "large"
    "--task", "translate",           # Translate to English
    "--language", "ja",              # Source language is Japanese
    "--vad_filter", "True",          # Skip silence
    "--compute_type", "int8",        # Quantization for speed/GPU memory
    "--output_format", "srt",        # SRT subtitle format
    "--output_dir", os.path.dirname(os.path.abspath(input_vid))
]

# Execute subtitle generation
subprocess.run(whisper_cmd, creationflags=LOW_PRIORITY)

# ========== STAGE 3: MUXING (FAST) ==========
if os.path.exists(srt_file):
    print("\n" + "="*60)
    print("▶️  [3/3] Muxing subtitles into final MKV...")
    print("="*60 + "\n")
    
    final_output = output_vid.replace(".mkv", "_final.mkv")
    
    # Build muxing command
    mux_cmd = [
        ffmpeg_path, "-i", output_vid, "-i", srt_file,
        "-map", "0", "-map", "1",  # Include all streams from both files
        "-c", "copy",              # Copy (don't re-encode)
        "-c:s", "srt",             # Subtitle codec
        "-metadata:s:s:0", "language=eng",
        "-metadata:s:s:0", "title=AI English Translation",
        final_output
    ]
    
    # Execute muxing (fast, runs at normal priority)
    subprocess.run(mux_cmd)
    print(f"\n✅ Success! Final file: {final_output}")
else:
    print("\n⚠️  Warning: Subtitle file not found. Whisper step may have failed.")
    print("   Check the output above for error messages.")

# ========== OPTIONAL: SHUTDOWN PC ==========
if halt == 'y':
    print("\n⏻️  System shutting down in 60 seconds...")
    os.system("shutdown /s /t 60")