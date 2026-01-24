"""
===================================
BENCHMARK TOOL
===================================
benchmark.py

Lightweight benchmarking tool that tests 4 preset options without full encoding.
Useful for testing new hardware or getting quick estimates.

⚠️ BETTER ALTERNATIVE: Use encode_smart.py which does the same thing
   but also handles the full encoding after benchmarking.

This script:
1. Tests 8-second clips with 4 different presets
2. Shows time and size estimates
3. Exits (doesn't encode full video)

USAGE (Direct Python):
  python benchmark.py <input>

USAGE (Wrapper Scripts - Recommended):
  Windows PowerShell: .\benchmark.ps1 input.mp4
  Linux/macOS:       ./benchmark.sh input.mp4

EXAMPLES:
  python benchmark.py input.mp4
  .\benchmark.ps1 video.mkv
  ./benchmark.sh sample.mp4
"""

import sys
import subprocess
import os
import time

# ========== HELPER FUNCTIONS ==========

def get_duration(file):
    """
    Extract total video duration using ffprobe.
    """
    cmd = [
        "ffprobe", "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        file
    ]
    return float(subprocess.check_output(cmd).decode().strip())


def estimate(input_file, res, preset, crf, total_duration):
    """
    Benchmark a specific encoding preset.
    
    Tests only 8 seconds to quickly estimate full encode time and output size.
    See convert2.py for detailed documentation.
    """
    ffmpeg_path = "ffmpeg"
    output_test = "test_bench.mkv"
    scale = f"scale=-2:{res}:flags=lanczos" if res != "source" else "null"
    
    cmd = [
        ffmpeg_path, "-y", "-i", input_file, "-t", "8",
        "-vf", scale, 
        "-c:v", "libsvtav1", 
        "-preset", str(preset), 
        "-crf", str(crf),
        "-c:a", "libopus", 
        output_test
    ]
    
    # Run benchmark
    start_time = time.time()
    subprocess.run(cmd, capture_output=True)
    end_time = time.time()
    
    # Calculate speed and estimates
    speed = 8 / (end_time - start_time)
    est_hours = (total_duration / speed) / 3600
    source_size_gb = os.path.getsize(input_file) / (1024**3)
    factor = 0.17 * (2 ** ((int(crf) - 30) / 10))
    if res == "720": 
        factor *= 0.6
    est_gb = source_size_gb * factor

    # Clean up
    if os.path.exists(output_test): 
        os.remove(output_test)
    return est_hours, est_gb


# ========== MAIN EXECUTION ==========

if len(sys.argv) < 2:
    print("Usage: python bench.py input.mp4")
    sys.exit(1)

input_vid = sys.argv[1]
duration = get_duration(input_vid)

print(f"\n--- Benchmarking Ryzen 2600 ({duration/60:.1f} min video) ---\n")

# Test 4 preset options
options = [
    ("source", 6, 30, "YOUR PREFERRED"),
    ("source", 8, 36, "Faster Encode"),
    ("720", 8, 32, "Clear/Small"),
    ("720", 10, 40, "Ultra Fast")
]

for i, (res, p, crf, label) in enumerate(options, 1):
    h, s = estimate(input_vid, res, p, crf, duration)
    print(f"{i}) {res:6} | {label:15} (P{p}/CRF{crf}) -> Est: {h:5.1f} hrs | {s:5.1f} GB")

print("\n📝 Next step: Use convert2.py to encode and pick your preferred option")
print("   python convert2.py <input> <output>")