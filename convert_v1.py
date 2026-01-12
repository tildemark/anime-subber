import sys
import subprocess
import os

if len(sys.argv) < 3:
    print("Usage: python convert.py input.mp4 output.mkv [resolution]")
    print("Example: python convert.py vid.mp4 out.mkv 1440")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
# Check if a 3rd argument (resolution) was provided
target_res = sys.argv[3] if len(sys.argv) > 3 else None

script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe")

command = [
    ffmpeg_path, "-i", input_file
]

# Resolution logic
if target_res:
    # Scale to target height (e.g., 1440), calculate width automatically (-2)
    command.extend(["-vf", f"scale=-2:{target_res}:flags=lanczos"])
    print(f"Targeting resolution: {target_res}p")
else:
    print("No resolution specified. Keeping original size.")

# Add encoding parameters
command.extend([
    "-c:v", "libsvtav1",
    "-preset", "8",
    "-crf", "30",
    "-svtav1-params", "tune=0:enable-overlays=1",
    "-c:a", "libopus", "-b:a", "128k",
    output_file
])

# Run with 'Low Priority' to keep your Ryzen 2600 responsive for other tasks
if os.name == 'nt': # If on Windows
    # CREATE_LOW_PRIORITY_CONTROL_SET = 0x00004000
    subprocess.run(command, creationflags=0x00004000)
else:
    subprocess.run(command)