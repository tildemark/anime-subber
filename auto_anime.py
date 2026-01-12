import sys
import subprocess
import os

if os.name == 'nt':
    print("❌ Error: This version of the script is for Linux/macOS.")
    print("👉 Please use 'auto_anime_win.py' for Windows.")
    sys.exit(1)

if len(sys.argv) < 3:
    print("Usage: python auto_anime.py input.mp4 output.mkv [resolution]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
target_res = sys.argv[3] if len(sys.argv) > 3 else None

# Creation flag for Low Priority on Windows (prevents system lag)
LOW_PRIORITY = 0x00004000 if os.name == 'nt' else 0
ffmpeg_path = "ffmpeg"

# --- STAGE 1: VIDEO CONVERSION (CPU) ---
print(f"\n[1/3] Stage 1: Converting video to AV1...")
video_cmd = [ffmpeg_path, "-i", input_file]
if target_res:
    video_cmd.extend(["-vf", f"scale=-2:{target_res}:flags=lanczos"])

video_cmd.extend([
    "-c:v", "libsvtav1", "-preset", "8", "-crf", "30",
    "-svtav1-params", "tune=0:enable-overlays=1",
    "-c:a", "libopus", "-b:a", "128k",
    output_file
])
subprocess.run(video_cmd, creationflags=LOW_PRIORITY)

# --- STAGE 2: AI TRANSLATION (GPU) ---
print(f"\n[2/3] Stage 2: Generating AI Subtitles (Whisper)...")
# Note: Whisper will output the .srt file in the same directory as the input
srt_file = os.path.splitext(input_file)[0] + ".srt"

whisper_cmd = [
    "whisper-ctranslate2", input_file,
    "--model", "small",          # Recommended for 2GB VRAM
    "--task", "translate",
    "--language", "ja",
    "--vad_filter", "True",      # Skips action scenes/silence
    "--compute_type", "int8",    # Optimized for 10-series GPUs
    "--output_format", "srt",
    "--output_dir", os.path.dirname(os.path.abspath(input_file))
]
subprocess.run(whisper_cmd, creationflags=LOW_PRIORITY)

# --- STAGE 3: MUXING (COMBINE) ---
if os.path.exists(srt_file):
    print(f"\n[3/3] Stage 3: Muxing subtitles into final MKV...")
    # Add a suffix so we don't overwrite our new AV1 file
    final_output = output_file.replace(".mkv", "_subbed.mkv")
    
    mux_cmd = [
        ffmpeg_path, "-i", output_file, "-i", srt_file,
        "-map", "0", "-map", "1", 
        "-c", "copy", "-c:s", "srt",
        "-metadata:s:s:0", "language=eng", 
        "-metadata:s:s:0", "title=AI English Translation",
        final_output
    ]
    subprocess.run(mux_cmd, creationflags=LOW_PRIORITY)
    print(f"\nDone! Process complete. Final file: {final_output}")
else:
    print(f"\nError: Subtitle file {srt_file} was not found. Skipping Stage 3.")