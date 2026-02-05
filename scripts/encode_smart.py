"""
=========================================================
INTERACTIVE CONVERTER WITH BENCHMARKING
=========================================================
encode_smart.py

ADVANCED version with real-time benchmarking and smart options.
This script:
1. Benchmarks your hardware with 4 different presets
2. Shows estimated encoding time and output file size
3. Lets you pick the best option interactively
4. Can auto-shutdown PC when done
5. BATCH MODE: Supports wildcard patterns (*.mp4, videos/*.mkv)

BEST FOR: When you want to optimize settings for your specific hardware
          and choose between speed vs quality tradeoffs

USAGE (Direct Python):
  python encode_smart.py <input> [output]
  python encode_smart.py "*.mp4"

USAGE (Wrapper Scripts - Recommended):
  Windows PowerShell: .\encode_smart.ps1 input.mp4
  Linux/macOS:       ./encode_smart.sh input.mp4

EXAMPLES:
  python encode_smart.py input.mkv output.mkv
  .\encode_smart.ps1 "season1/*.mp4"
  ./encode_smart.sh input.mp4 output.mkv
"""

import sys
import subprocess
import os
import time
from glob import glob

# ========== PATH HELPERS ==========

def get_ffmpeg_path():
    """Return bundled ffmpeg.exe if present, otherwise use PATH."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(script_dir, "ffmpeg.exe") if os.name == 'nt' else "ffmpeg"
    if os.name == 'nt' and os.path.exists(local_ffmpeg):
        return local_ffmpeg
    return "ffmpeg"

# ========== HELPER FUNCTIONS ==========

def get_duration(file):
    """Uses ffprobe to extract the total video duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        file
    ]
    return float(subprocess.check_output(cmd).decode().strip())


def estimate(input_file, res, preset, crf, total_duration, use_gpu=False):
    """Benchmark a specific encoding preset on your hardware.

    use_gpu=False  -> CPU encode with libsvtav1
    use_gpu=True   -> GPU encode with hevc_nvenc (NVENC HEVC)
    """
    ffmpeg_path = get_ffmpeg_path()
    output_test = "test_bench.mkv"
    
    scale = f"scale=-2:{res}:flags=lanczos" if res != "source" else "null"
    
    cmd = [ffmpeg_path, "-y", "-i", input_file, "-t", "8", "-vf", scale]

    if use_gpu:
        gpu_preset = {"6": "slow", "8": "medium", "10": "fast"}.get(str(preset), "medium")
        cmd += [
            "-c:v", "hevc_nvenc",
            "-preset", gpu_preset,
            "-rc", "vbr_hq",
            "-cq", str(crf),
            "-b:v", "0",
        ]
    else:
        cmd += [
            "-c:v", "libsvtav1", 
            "-preset", str(preset), 
            "-crf", str(crf),
        ]

    cmd += [
        "-c:a", "libopus", 
        output_test
    ]
    
    print(f"  Benchmarking: {res}p | Preset {preset} | CRF {crf}...", end=" ", flush=True)
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True)
    end_time = time.time()

    elapsed = end_time - start_time
    if elapsed <= 0:
        elapsed = 0.01
    speed = 8 / elapsed
    est_hours = (total_duration / speed) / 3600
    
    try:
        source_size_gb = os.path.getsize(input_file) / (1024**3)
        factor = 0.17 * (2 ** ((int(crf) - 30) / 10))
        if res == "720": 
            factor *= 0.6
        est_gb = source_size_gb * factor
    except:
        est_gb = (12 * (total_duration / 60) * (2 ** ((30 - crf) / 10))) / 1024

    if os.path.exists(output_test): 
        os.remove(output_test)
    
    if result.returncode != 0:
        print(f"⚠ (ffmpeg error {result.returncode}) {est_hours:.1f}h | {est_gb:.1f}GB")
    else:
        print(f"✓ {est_hours:.1f}h | {est_gb:.1f}GB")
    return est_hours, est_gb


def encode_file(input_vid, output_vid, settings, use_gpu=False):
    """Encode a single file with chosen settings.

    use_gpu=False  -> CPU encode with libsvtav1
    use_gpu=True   -> GPU encode with hevc_nvenc (NVENC HEVC)
    """
    ffmpeg_path = get_ffmpeg_path()
    
    scale = f"scale=-2:{settings['res']}:flags=lanczos" if settings['res'] != "source" else "null"
    
    cmd = [ffmpeg_path, "-i", input_vid, "-vf", scale]

    if use_gpu:
        gpu_preset = {"6": "slow", "8": "medium", "10": "fast"}.get(str(settings['p']), "medium")
        cmd += [
            "-c:v", "hevc_nvenc",
            "-preset", gpu_preset,
            "-rc", "vbr_hq",
            "-cq", str(settings['crf']),
            "-b:v", "0",
            "-metadata", f"comment=Converted HEVC NVENC preset {gpu_preset} CQ{settings['crf']}",
        ]
    else:
        cmd += [
            "-c:v", "libsvtav1", 
            "-preset", settings['p'], 
            "-crf", settings['crf'],
            "-svtav1-params", "tune=0:enable-overlays=1:lookahead=120",
            "-metadata", f"comment=Converted SVT-AV1 P{settings['p']} CRF{settings['crf']}",
        ]

    cmd += [
        "-c:a", "libopus", "-b:a", "128k",
        output_vid
    ]
    
    if os.name == 'nt':
        subprocess.run(cmd, creationflags=0x00004000)
    else:
        subprocess.run(["nice", "-n", "15"] + cmd)


# ========== MAIN EXECUTION ==========

if len(sys.argv) < 2:
    print("Usage: python convert2.py <input> [output]")
    print("Examples:")
    print("  Single file:  python convert2.py input.mp4 output.mkv")
    print("  Batch:        python convert2.py \"*.mp4\"")
    sys.exit(1)

input_pattern = sys.argv[1]
output_spec = sys.argv[2] if len(sys.argv) > 2 else None

# ========== BATCH MODE DETECTION ==========
files = glob(input_pattern)

if not files:
    print(f"❌ No files matched: {input_pattern}")
    sys.exit(1)

if len(files) > 1:
    # BATCH MODE - Run smart benchmark once, apply choice to all
    print(f"\n{'='*60}")
    print(f"🔄 BATCH MODE - Processing {len(files)} files")
    print(f"{'='*60}\n")

    sample_vid = files[0]
    duration = get_duration(sample_vid)

    print(f"Using first file as sample for benchmarking:")
    print(f"📁 Sample File: {sample_vid}")
    print(f"📊 Duration: {duration/60:.1f} minutes\n")

    use_gpu = input("⚙️  Use GPU encoder (NVENC HEVC) instead of CPU SVT-AV1 for this batch? (y/n): ").strip().lower().startswith('y')
    if use_gpu:
        print("\n➡ Using GPU: HEVC NVENC encoder for all files in batch.\n")
    else:
        print("\n➡ Using CPU: SVT-AV1 encoder for all files in batch.\n")

    print("🔄 Running benchmarks on sample file (this may take 30-60 seconds)...\n")

    h1, s1 = estimate(sample_vid, "source", 6, 30, duration, use_gpu=use_gpu)
    h2, s2 = estimate(sample_vid, "source", 8, 36, duration, use_gpu=use_gpu)
    h3, s3 = estimate(sample_vid, "720", 8, 32, duration, use_gpu=use_gpu)
    h4, s4 = estimate(sample_vid, "720", 10, 40, duration, use_gpu=use_gpu)
    h5, s5 = estimate(sample_vid, "720", 8, 40, duration, use_gpu=use_gpu)
    h6, s6 = estimate(sample_vid, "720", 6, 40, duration, use_gpu=use_gpu)

    print("\n" + "="*60)
    print("📋 CHOOSE YOUR PREFERRED ENCODING OPTION FOR THE BATCH:\n")
    print(f"1) 1080p | YOUR PREFERRED (P6 / CRF 30)")
    print(f"   └─ Time: {h1:.1f}h | Size: {s1:.1f}GB | ✓ BEST QUALITY\n")
    print(f"2) 1080p | Faster Encode (P8 / CRF 36)")
    print(f"   └─ Time: {h2:.1f}h | Size: {s2:.1f}GB | ⚡ 2x FASTER\n")
    print(f"3) 720p  | Clear/Small (P8 / CRF 32)")
    print(f"   └─ Time: {h3:.1f}h | Size: {s3:.1f}GB | 📉 BALANCED\n")
    print(f"4) 720p  | Ultra Fast (P10 / CRF 40)")
    print(f"   └─ Time: {h4:.1f}h | Size: {s4:.1f}GB | 💨 FASTEST\n")
    print(f"5) 720p  | Smallest (P8 / CRF 40)")
    print(f"   └─ Time: {h5:.1f}h | Size: {s5:.1f}GB | 📦 SMALLEST\n")
    print(f"6) 720p  | High Quality Small (P6 / CRF 40)")
    print(f"   └─ Time: {h6:.1f}h | Size: {s6:.1f}GB | 🎯 SHARPER\n")
    print("="*60)

    choice = input("\n👉 Selection for entire batch (1-6): ").strip()

    settings_map = {
        "1": {"res": "source", "p": "6",  "crf": "30"},
        "2": {"res": "source", "p": "8",  "crf": "36"},
        "3": {"res": "720",    "p": "8",  "crf": "32"},
        "4": {"res": "720",    "p": "10", "crf": "40"},
        "5": {"res": "720",    "p": "8",  "crf": "40"},
        "6": {"res": "720",    "p": "6",  "crf": "40"}
    }

    if choice not in settings_map:
        print("❌ Invalid choice. Aborting batch.")
        sys.exit(1)

    chosen_settings = settings_map[choice]
    do_shutdown = input("⏻️  Shutdown PC when finished with batch? (y/n): ").lower() == 'y'

    for i, input_file in enumerate(files, 1):
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_encoded.mkv"

        print(f"\n[{i}/{len(files)}] Encoding: {input_file}")
        print(f"Output: {output_file}\n")

        encode_file(input_file, output_file, chosen_settings, use_gpu=use_gpu)
        print(f"✅ Complete\n")

    print(f"\n{'='*60}")
    print(f"✅ Batch conversion complete! All {len(files)} files processed.")
    print(f"{'='*60}")

    if do_shutdown:
        print("\n⏻️  System shutting down in 60 seconds...")
        os.system("shutdown /s /t 60" if os.name == 'nt' else "shutdown -h +1")

else:
    # SINGLE FILE MODE - Interactive
    input_vid = files[0]
    duration = get_duration(input_vid)

    print(f"\n╔════════════════════════════════════════════╗")
    print(f"║   ANIME CONVERTER V2 - Smart Benchmarking  ║")
    print(f"╚════════════════════════════════════════════╝")
    print(f"\n📊 Video Duration: {duration/60:.1f} minutes")
    print(f"📁 Input File: {input_vid}\n")

    use_gpu = input("⚙️  Use GPU encoder (NVENC HEVC) instead of CPU SVT-AV1? (y/n): ").strip().lower().startswith('y')
    if use_gpu:
        print("\n➡ Using GPU: HEVC NVENC encoder (much faster, larger files).\n")
    else:
        print("\n➡ Using CPU: SVT-AV1 encoder (slower, higher efficiency).\n")

    print("🔄 Running benchmarks (this may take 30-60 seconds)...\n")

    h1, s1 = estimate(input_vid, "source", 6, 30, duration, use_gpu=use_gpu)
    h2, s2 = estimate(input_vid, "source", 8, 36, duration, use_gpu=use_gpu)
    h3, s3 = estimate(input_vid, "720", 8, 32, duration, use_gpu=use_gpu)
    h4, s4 = estimate(input_vid, "720", 10, 40, duration, use_gpu=use_gpu)
    h5, s5 = estimate(input_vid, "720", 8, 40, duration, use_gpu=use_gpu)
    h6, s6 = estimate(input_vid, "720", 6, 40, duration, use_gpu=use_gpu)

    print("\n" + "="*60)
    print("📋 CHOOSE YOUR PREFERRED ENCODING OPTION:\n")
    print(f"1) 1080p | YOUR PREFERRED (P6 / CRF 30)")
    print(f"   └─ Time: {h1:.1f}h | Size: {s1:.1f}GB | ✓ BEST QUALITY\n")
    print(f"2) 1080p | Faster Encode (P8 / CRF 36)")
    print(f"   └─ Time: {h2:.1f}h | Size: {s2:.1f}GB | ⚡ 2x FASTER\n")
    print(f"3) 720p  | Clear/Small (P8 / CRF 32)")
    print(f"   └─ Time: {h3:.1f}h | Size: {s3:.1f}GB | 📉 BALANCED\n")
    print(f"4) 720p  | Ultra Fast (P10 / CRF 40)")
    print(f"   └─ Time: {h4:.1f}h | Size: {s4:.1f}GB | 💨 FASTEST\n")
    print(f"5) 720p  | Smallest (P8 / CRF 40)")
    print(f"   └─ Time: {h5:.1f}h | Size: {s5:.1f}GB | 📦 SMALLEST\n")
    print(f"6) 720p  | High Quality Small (P6 / CRF 40)")
    print(f"   └─ Time: {h6:.1f}h | Size: {s6:.1f}GB | 🎯 SHARPER\n")
    print("="*60)

    choice = input("\n👉 Selection (1-6): ").strip()
    do_shutdown = input("⏻️  Shutdown PC when finished? (y/n): ").lower() == 'y'

    settings = {
        "1": {"res": "source", "p": "6",  "crf": "30"},
        "2": {"res": "source", "p": "8",  "crf": "36"},
        "3": {"res": "720",    "p": "8",  "crf": "32"},
        "4": {"res": "720",    "p": "10", "crf": "40"},
        "5": {"res": "720",    "p": "8",  "crf": "40"},
        "6": {"res": "720",    "p": "6",  "crf": "40"}
    }

    if choice in settings:
        c = settings[choice]
        
        if output_spec is None:
            base_name = os.path.splitext(os.path.basename(input_vid))[0]
            output_vid = f"{base_name}_encoded.mkv"
        else:
            output_vid = output_spec

        print(f"\n▶️  Starting Final Conversion (Option {choice})...")
        print(f"   Encoding to {c['res']}p | Preset {c['p']} | CRF {c['crf']}\n")

        encode_file(input_vid, output_vid, c, use_gpu=use_gpu)
        
        print(f"\n✅ Conversion complete!")
        print(f"📁 Output: {output_vid}")
        
        if do_shutdown:
            print("\n⏻️  System shutting down in 60 seconds...")
            os.system("shutdown /s /t 60" if os.name == 'nt' else "shutdown -h +1")
    else:
        print("❌ Invalid choice.")
