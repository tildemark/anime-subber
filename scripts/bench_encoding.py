"""
===============================================
ENCODING BENCHMARK UTILITY
===============================================
bench_encoding.py

Specialized benchmarking tool for detailed encoding parameter testing.
Tests various preset/CRF combinations to help optimize your settings.

USAGE (Direct Python):
  python bench_encoding.py <input>

USAGE (Wrapper Scripts - Recommended):
  Windows PowerShell: .\bench_encoding.ps1 input.mp4
  Linux/macOS:       ./bench_encoding.sh input.mp4

EXAMPLES:
  python bench_encoding.py input.mp4
  .\bench_encoding.ps1 video.mkv
  ./bench_encoding.sh sample.mp4
"""

import sys
import subprocess
import os
import time

def get_duration(file):
    # Uses ffprobe to get the total length of the video in seconds
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file]
    return float(subprocess.check_output(cmd).decode().strip())

def estimate(input_file, res, preset, crf, total_duration):
    # Benchmark function optimized for Ryzen 2600
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe")
    output_test = "test_bench.mkv"
    
    scale = f"scale=-2:{res}:flags=lanczos" if res != "source" else "null"
    
    cmd = [
        ffmpeg_path, "-y", "-i", input_file, "-t", "8", # 8 sec test
        "-vf", scale, "-c:v", "libsvtav1", "-preset", str(preset), "-crf", str(crf),
        "-c:a", "libopus", output_test
    ]
    
    start_time = time.time()
    subprocess.run(cmd, capture_output=True)
    end_time = time.time()
    
    speed = 8 / (end_time - start_time)
    est_hours = (total_duration / speed) / 3600
    
    # Updated Size Logic based on your 5.8GB -> 1GB result (~17% retention)
    try:
        source_size_gb = os.path.getsize(input_file) / (1024**3)
        # Scale retention factor based on CRF and Resolution
        factor = 0.17 * (2 ** ((int(crf) - 30) / 10))
        if res == "720": factor *= 0.6
        est_gb = source_size_gb * factor
    except:
        est_gb = (12 * (total_duration / 60) * (2 ** ((30 - crf) / 10))) / 1024

    if os.path.exists(output_test): os.remove(output_test)
    return est_hours, est_gb

# --- MAIN ---
if len(sys.argv) < 3:
    print("Usage: python convert.py input.mp4 output.mkv")
    sys.exit(1)

input_vid, output_vid = sys.argv[1], sys.argv[2]
duration = get_duration(input_vid)

print(f"\n--- Benchmarking Ryzen 2600 ({duration/60:.1f} min video) ---")

# Options calibrated for your specific hardware and goals
h1, s1 = estimate(input_vid, "source", 6, 30, duration) # YOUR SUCCESSFUL SETUP
h2, s2 = estimate(input_vid, "source", 8, 36, duration) # Faster, slightly larger
h3, s3 = estimate(input_vid, "720", 8, 32, duration)    # 720p Balanced
h4, s4 = estimate(input_vid, "720", 10, 40, duration)   # 720p Tiny

print("\nCHOOSE YOUR OPTION:")
print(f"1) 1080p | YOUR PREFERRED (P6 / CRF 30) -> Est: {h1:.1f} hrs | ~{s1:.1f} GB")
print(f"2) 1080p | Faster Encode  (P8 / CRF 36) -> Est: {h2:.1f} hrs | ~{s2:.1f} GB")
print(f"3) 720p  | Clear/Small    (P8 / CRF 32) -> Est: {h3:.1f} hrs | ~{s3:.1f} GB")
print(f"4) 720p  | Ultra Fast     (P10/ CRF 40) -> Est: {h4:.1f} hrs | ~{s4:.1f} GB")

choice = input("\nSelection (1-4): ")
do_shutdown = input("Shutdown PC when finished? (y/n): ").lower() == 'y'

settings = {
    "1": {"res": "source", "p": "6",  "crf": "30"},
    "2": {"res": "source", "p": "8",  "crf": "36"},
    "3": {"res": "720",    "p": "8",  "crf": "32"},
    "4": {"res": "720",    "p": "10", "crf": "40"}
}

if choice in settings:
    c = settings[choice]
    scale = f"scale=-2:{c['res']}:flags=lanczos" if c['res'] != "source" else "null"
    
    cmd = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe"),
        "-i", input_vid,
        "-vf", scale,
        "-c:v", "libsvtav1", "-preset", c['p'], "-crf", c['crf'],
        "-svtav1-params", "tune=0:enable-overlays=1:lookahead=120",
        "-metadata", f"comment=Converted SVT-AV1 P{c['p']} CRF{c['crf']}",
        "-c:a", "libopus", "-b:a", "128k",
        output_vid
    ]
    
    print(f"\nStarting Final Conversion (Option {choice})...")
    # Creation flag 0x00004000 = Low Priority for Windows
    try:
        subprocess.run(cmd, creationflags=0x00004000)
        
        if do_shutdown:
            print("\nConversion complete! Shutting down in 60 seconds...")
            os.system("shutdown /s /t 60")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("Invalid choice.")