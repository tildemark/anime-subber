"""
===============================================
SUBTITLE-ONLY CONVERTER
===============================================
add_subtitles.py

Use this when you ONLY need to add subtitles to an existing video.
This is faster than full pipeline because it skips video encoding.

WORKFLOW: 
  1. Generate AI subtitles (Whisper) 
  2. Mux subtitles into MKV

BEST FOR:
  - You already have an AV1-encoded video
  - You just want to add/update subtitles
  - Fast turnaround needed
  - BATCH: Process multiple encoded videos

DIFFERENCES FROM pipeline_windows.py:
  - No video re-encoding (saves ~90% of time)
  - Only generates & muxes subtitles
  - Requires input video to already be encoded

DEPENDENCIES: ffmpeg, whisper-ctranslate2

USAGE (Direct Python):
  python add_subtitles.py <input_video> [output_mkv]
  python add_subtitles.py "*.mkv"

USAGE (Wrapper Scripts - Recommended):
  Windows PowerShell: .\add_subtitles.ps1 encoded.mkv
  Linux/macOS:       ./add_subtitles.sh encoded.mkv

EXAMPLES:
  python add_subtitles.py already_encoded.mkv final.mkv
  .\add_subtitles.ps1 video.mp4 output.mkv
  ./add_subtitles.sh "*.mp4"  (batch mode)
"""

import sys
import subprocess
import os
from glob import glob

# ========== SAFETY CHECK ==========
# This script is Windows-only
if os.name != 'nt':
    print("❌ Error: This script is for Windows.")
    sys.exit(1)

# ========== ARGUMENT PARSING ==========
if len(sys.argv) < 2:
    print("\n" + "="*60)
    print("  SUBTITLE-ONLY CONVERTER (Windows)")
    print("="*60)
    print("\nUsage: python translate_only.py <input_video> [output_mkv]")
    print("Examples:")
    print("  python translate_only.py video.mp4 final.mkv")
    print("  python translate_only.py encoded.mkv subbed.mkv")
    print("  python translate_only.py \"*.mp4\"  (batch mode)")
    sys.exit(1)

input_pattern = sys.argv[1]
output_spec = sys.argv[2] if len(sys.argv) > 2 else None

# ========== HELPER FUNCTION ==========
def process_file(input_vid, output_vid):
    """Process a single video file for subtitles only"""
    LOW_PRIORITY = 0x00004000
    ffmpeg_path = "ffmpeg"
    input_dir = os.path.dirname(os.path.abspath(input_vid))
    input_filename_no_ext = os.path.splitext(os.path.basename(input_vid))[0]

    # ========== STAGE 1: AI TRANSLATION (GPU INTENSIVE) ==========
    print(f"\n{'='*60}")
    print(f"▶️  [1/2] Translating: {input_filename_no_ext}")
    print(f"{'='*60}")
    print("Mode: Whisper Medium Model")
    print("Task: Japanese → English Translation\n")

    whisper_cmd = [
        "whisper-ctranslate2", 
        input_vid,
        "--task", "translate",
        "--language", "ja",
        "--model", "medium",
        "--beam_size", "5",
        "--vad_filter", "True",
        "--compute_type", "int8",
        "--device", "cuda",
        "--output_format", "srt",
        "--output_dir", input_dir
    ]

    print("Processing audio... (this may take 10-30 minutes)\n")
    try:
        result = subprocess.run(whisper_cmd, creationflags=LOW_PRIORITY)
        if result.returncode != 0:
            print("\n❌ Whisper process failed.")
            return None
    except Exception as e:
        print(f"❌ Execution Error: {e}")
        return None

    # ========== STAGE 2: SRT FILE DETECTION ==========
    potential_srt_paths = [
        os.path.join(input_dir, f"{input_filename_no_ext}.srt"),
        os.path.join(input_dir, input_filename_no_ext, f"{input_filename_no_ext}.srt")
    ]

    srt_file = None
    for path in potential_srt_paths:
        if os.path.exists(path):
            srt_file = path
            print(f"✓ Found subtitles: {os.path.basename(srt_file)}\n")
            break

    # ========== STAGE 3: MUXING (COMBINING VIDEO + SUBTITLES) ==========
    if srt_file:
        print(f"{'='*60}")
        print(f"▶️  [2/2] Muxing subtitles into final MKV...")
        print(f"{'='*60}\n")
        
        if not output_vid.lower().endswith(".mkv"):
            output_vid = os.path.splitext(output_vid)[0] + ".mkv"

        mux_cmd = [
            ffmpeg_path,
            "-y",
            "-i", input_vid,
            "-i", srt_file,
            "-map", "0", "-map", "1",
            "-c", "copy",
            "-c:s", "srt",
            "-metadata:s:s:0", "language=eng",
            "-metadata:s:s:0", "title=AI English Translation (Whisper Medium)",
            output_vid
        ]
        
        print("Muxing subtitles into video...\n")
        subprocess.run(mux_cmd)
        
        print(f"{'='*60}")
        print(f"✅ SUCCESS!")
        print(f"{'='*60}")
        print(f"Final subbed file: {output_vid}\n")
        return output_vid
    else:
        print(f"\n❌ Error: Could not locate the generated .srt file.")
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
    
    for i, input_file in enumerate(files, 1):
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_subbed.mkv"
        
        print(f"\n{'─'*60}")
        print(f"[{i}/{len(files)}] Processing: {input_file}")
        print(f"{'─'*60}")
        
        process_file(input_file, output_file)
    
    print(f"\n{'='*60}")
    print(f"✅ Batch subtitle processing complete! All {len(files)} files processed.")
    print(f"{'='*60}")

else:
    # SINGLE FILE MODE
    input_vid = os.path.abspath(files[0])
    
    if output_spec is None:
        base_name = os.path.splitext(os.path.basename(input_vid))[0]
        output_vid = f"{base_name}_subbed.mkv"
    else:
        output_vid = os.path.abspath(output_spec)
    
    process_file(input_vid, output_vid)