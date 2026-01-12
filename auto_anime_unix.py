import sys
import subprocess
import os
import platform

# Safety check: Ensure this isn't running on Windows
if os.name == 'nt':
    print("❌ Error: This script is optimized for Linux and macOS.")
    print("👉 Please use 'auto_anime_win.py' for Windows systems.")
    sys.exit(1)

if len(sys.argv) < 3:
    print("Usage: python auto_anime_unix.py input.mp4 output.mkv [resolution]")
    print("Example: python auto_anime_unix.py movie.mp4 out.mkv 1080")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
target_res = sys.argv[3] if len(sys.argv) > 3 else None

# Path to ffmpeg (usually just 'ffmpeg' on Unix)
ffmpeg_path = "ffmpeg"

def run_low_priority(cmd):
    """
    On Unix, we use the 'nice' command to lower the process priority.
    A value of 15 ensures the system remains responsive for other tasks.
    """
    return subprocess.run(["nice", "-n", "15"] + cmd)

# --- STAGE 1: VIDEO CONVERSION (CPU) ---
print(f"\n[1/3] Stage 1: Converting video to AV1 on {platform.system()}...")

video_cmd = [ffmpeg_path, "-i", input_file]

if target_res:
    # Scale to target height, calculate width automatically
    video_cmd.extend(["-vf", f"scale=-2:{target_res}:flags=lanczos"])
    print(f"Targeting resolution: {target_res}p")

video_cmd.extend([
    "-c:v", "libsvtav1",
    "-preset", "8",
    "-crf", "30",
    "-svtav1-params", "tune=0:enable-overlays=1",
    "-c:a", "libopus", "-b:a", "128k",
    output_file
])

run_low_priority(video_cmd)

# --- STAGE 2: AI SUBTITLE GENERATION (GPU/CPU) ---
print(f"\n[2/3] Stage 2: Generating AI Subtitles (Japanese -> English)...")

# Define the SRT path based on the input filename
srt_file = os.path.splitext(input_file)[0] + ".srt"

whisper_cmd = [
    "whisper-ctranslate2", input_file,
    "--model", "small",
    "--task", "translate",
    "--language", "ja",
    "--vad_filter", "True",      # Critical for long movies with action/silence
    "--compute_type", "int8",    # Efficient for most hardware
    "--output_format", "srt",
    "--output_dir", os.path.dirname(os.path.abspath(input_file))
]

# Run whisper with low priority
run_low_priority(whisper_cmd)

# --- STAGE 3: MUXING (COMBINING) ---
if os.path.exists(srt_file):
    print(f"\n[3/3] Stage 3: Muxing subtitles into final MKV...")
    
    # Create final output name to distinguish from stage 1 output
    final_output = output_file.replace(".mkv", "_subbed.mkv")
    
    mux_cmd = [
        ffmpeg_path, "-i", output_file, "-i", srt_file,
        "-map", "0", "-map", "1", 
        "-c", "copy", "-c:s", "srt",
        "-metadata:s:s:0", "language=eng", 
        "-metadata:s:s:0", "title=AI English Translation",
        final_output
    ]
    
    # Muxing is instant, no need for nice/priority
    subprocess.run(mux_cmd)
    
    print(f"\n✅ Done! Final movie created: {final_output}")
else:
    print(f"\n❌ Error: Subtitle file {srt_file} was not generated.")