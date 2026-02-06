"""
=========================================================
ANIME SUBBER - HYBRID GUI/CLI APPLICATION
=========================================================
main_app.py

A unified Windows Desktop Application using Gooey that:
- Launches a GUI if no arguments are passed
- Runs as a standard CLI if arguments are detected
- Supports both single file and batch folder processing
- Provides hardware options (CUDA/CPU, resolution, preset)
- Includes post-task shutdown management

USAGE (GUI Mode):
    python main_app.py
    # OR: main_app.exe (after PyInstaller packaging)

USAGE (CLI Mode):
    python main_app.py --input movie.mp4 --device cuda --resolution 1080
    python main_app.py --batch-folder "C:\Videos" --device cpu --shutdown

PACKAGING:
    pyinstaller --onefile --windowed --icon=icon.ico --name="AnimeSubber" main_app.py

DEPENDENCIES:
    pip install gooey whisper-ctranslate2
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
"""

import sys
import subprocess
import os
import time
import json
from glob import glob
from pathlib import Path

# Check if running in GUI mode (no CLI arguments)
if len(sys.argv) == 1:
    from gooey import Gooey, GooeyParser
    GUI_MODE = True
else:
    # CLI mode - use standard argparse
    from argparse import ArgumentParser as GooeyParser
    def Gooey(*args, **kwargs):
        """Dummy decorator for CLI mode"""
        def decorator(func):
            return func
        return decorator
    GUI_MODE = False

# ========== CONSTANTS ==========
LOW_PRIORITY = 0x00004000  # Windows: BELOW_NORMAL_PRIORITY_CLASS
SUPPORTED_VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']

# ========== HELPER FUNCTIONS ==========

def get_ffmpeg_path():
    """Return bundled ffmpeg.exe if present, otherwise use PATH."""
    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = sys._MEIPASS
        bundled_ffmpeg = os.path.join(bundle_dir, "ffmpeg.exe")
        if os.path.exists(bundled_ffmpeg):
            return bundled_ffmpeg
    
    # Check for ffmpeg in script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(script_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    
    # Fall back to system PATH
    return "ffmpeg"


def get_ffprobe_path():
    """Return bundled ffprobe.exe if present, otherwise use PATH."""
    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = sys._MEIPASS
        bundled_ffprobe = os.path.join(bundle_dir, "ffprobe.exe")
        if os.path.exists(bundled_ffprobe):
            return bundled_ffprobe
    
    # Check for ffprobe in script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffprobe = os.path.join(script_dir, "ffprobe.exe")
    if os.path.exists(local_ffprobe):
        return local_ffprobe
    
    # Fall back to system PATH
    return "ffprobe"


def get_duration(file):
    """Uses ffprobe to extract the total video duration in seconds."""
    ffprobe_path = get_ffprobe_path()
    cmd = [
        ffprobe_path, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file
    ]
    try:
        return float(subprocess.check_output(cmd).decode().strip())
    except:
        return 0


def get_video_files_from_folder(folder_path):
    """Get all video files from a folder."""
    video_files = []
    for ext in SUPPORTED_VIDEO_EXTENSIONS:
        video_files.extend(glob(os.path.join(folder_path, f"*{ext}")))
    return sorted(video_files)


# ========== STAGE 1: VIDEO ENCODING ==========

def encode_video(input_file, output_file, resolution, preset, crf=30):
    """
    Encode video using SVT-AV1 with low priority.
    
    Args:
        input_file: Path to input video
        output_file: Path to output video
        resolution: Target resolution (source, 1440, 1080, 720)
        preset: SVT-AV1 preset (0-13, lower=slower/better)
        crf: Constant Rate Factor (0-63, lower=better quality)
    """
    ffmpeg_path = get_ffmpeg_path()
    
    print(f"\n{'='*60}")
    print(f"▶️  [STAGE 1/3] Encoding Video: {os.path.basename(input_file)}")
    print(f"{'='*60}")
    print(f"Resolution: {resolution}p | Preset: {preset} | CRF: {crf}\n")
    
    # Build scaling filter
    if resolution == "source":
        scale = "null"
    else:
        scale = f"scale=-2:{resolution}:flags=lanczos"
    
    # Build encoding command
    cmd = [
        ffmpeg_path, "-i", input_file,
        "-vf", scale,
        "-c:v", "libsvtav1",
        "-preset", str(preset),
        "-crf", str(crf),
        "-svtav1-params", "tune=0:enable-overlays=1:lookahead=120",
        "-c:a", "libopus",
        "-b:a", "128k",
        "-metadata", f"comment=Converted SVT-AV1 P{preset} CRF{crf}",
        output_file
    ]
    
    # Execute with low priority
    subprocess.run(cmd, creationflags=LOW_PRIORITY)
    print(f"✅ Video encoding complete: {output_file}\n")


# ========== STAGE 2: AI SUBTITLE GENERATION ==========

def generate_subtitles(input_file, device="cuda"):
    """
    Generate English subtitles from Japanese audio using Whisper.
    
    Args:
        input_file: Path to video file
        device: 'cuda' or 'cpu'
    
    Returns:
        Path to generated SRT file, or None if failed
    """
    print(f"\n{'='*60}")
    print(f"▶️  [STAGE 2/3] Generating AI Subtitles")
    print(f"{'='*60}")
    print(f"Device: {device.upper()}\n")
    
    # Determine output SRT path
    base_name = os.path.splitext(input_file)[0]
    srt_file = f"{base_name}.srt"
    
    # IMPORTANT: For Windows, VAD filter parameters must be escaped as JSON string
    vad_params = json.dumps({"min_silence_duration_ms": 500})
    
    # Build Whisper command
    cmd = [
        "whisper-ctranslate2",
        input_file,
        "--model", "small",
        "--task", "translate",
        "--language", "ja",
        "--device", device,
        "--vad_filter", "True",
        "--vad_parameters", vad_params,  # Escaped JSON string
        "--compute_type", "int8",
        "--output_format", "srt",
        "--output_dir", os.path.dirname(os.path.abspath(input_file))
    ]
    
    # Execute subtitle generation
    result = subprocess.run(cmd, creationflags=LOW_PRIORITY)
    
    if result.returncode == 0 and os.path.exists(srt_file):
        print(f"✅ Subtitles generated: {srt_file}\n")
        return srt_file
    else:
        print(f"⚠️  Subtitle generation failed or file not found.\n")
        return None


# ========== STAGE 3: MUXING ==========

def mux_subtitles(video_file, srt_file, output_file):
    """
    Mux SRT subtitles into MKV container.
    
    Args:
        video_file: Path to encoded video
        srt_file: Path to SRT subtitle file
        output_file: Path to final output
    """
    ffmpeg_path = get_ffmpeg_path()
    
    print(f"\n{'='*60}")
    print(f"▶️  [STAGE 3/3] Muxing Subtitles")
    print(f"{'='*60}\n")
    
    cmd = [
        ffmpeg_path, "-i", video_file, "-i", srt_file,
        "-map", "0", "-map", "1",
        "-c", "copy",
        "-c:s", "srt",
        "-metadata:s:s:0", "language=eng",
        "-metadata:s:s:0", "title=AI English Translation",
        output_file
    ]
    
    subprocess.run(cmd)
    print(f"✅ Muxing complete: {output_file}\n")


# ========== MAIN PROCESSING LOGIC ==========

def process_single_file(input_file, device, resolution, preset, output_dir=None):
    """
    Process a single video file through the complete pipeline.
    
    Args:
        input_file: Path to input video
        device: 'cuda' or 'cpu'
        resolution: Target resolution
        preset: SVT-AV1 preset
        output_dir: Optional output directory (defaults to same as input)
    
    Returns:
        Path to final output file
    """
    print(f"\n{'#'*60}")
    print(f"# Processing: {os.path.basename(input_file)}")
    print(f"{'#'*60}\n")
    
    # Determine output paths
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        temp_video = os.path.join(output_dir, f"{base_name}_encoded.mkv")
        final_output = os.path.join(output_dir, f"{base_name}_final.mkv")
    else:
        input_dir = os.path.dirname(os.path.abspath(input_file))
        temp_video = os.path.join(input_dir, f"{base_name}_encoded.mkv")
        final_output = os.path.join(input_dir, f"{base_name}_final.mkv")
    
    # Stage 1: Encode video
    encode_video(input_file, temp_video, resolution, preset)
    
    # Stage 2: Generate subtitles
    srt_file = generate_subtitles(input_file, device)
    
    # Stage 3: Mux subtitles (if generated successfully)
    if srt_file and os.path.exists(srt_file):
        mux_subtitles(temp_video, srt_file, final_output)
        return final_output
    else:
        print(f"⚠️  Skipping muxing - using encoded video as final output")
        return temp_video


def process_batch(files, device, resolution, preset, shutdown_after):
    """
    Process multiple files in batch mode.
    
    Args:
        files: List of video file paths
        device: 'cuda' or 'cpu'
        resolution: Target resolution
        preset: SVT-AV1 preset
        shutdown_after: Whether to shutdown PC after completion
    """
    total = len(files)
    print(f"\n{'='*60}")
    print(f"🔄 BATCH MODE - Processing {total} files")
    print(f"{'='*60}\n")
    
    completed = []
    failed = []
    
    for i, input_file in enumerate(files, 1):
        print(f"\n[{i}/{total}] Starting: {os.path.basename(input_file)}")
        
        try:
            output_file = process_single_file(input_file, device, resolution, preset)
            completed.append(output_file)
            print(f"✅ [{i}/{total}] Complete: {os.path.basename(output_file)}")
        except Exception as e:
            failed.append(input_file)
            print(f"❌ [{i}/{total}] Failed: {os.path.basename(input_file)}")
            print(f"   Error: {str(e)}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Completed: {len(completed)}/{total}")
    if failed:
        print(f"❌ Failed: {len(failed)}/{total}")
        for f in failed:
            print(f"   - {os.path.basename(f)}")
    print(f"{'='*60}\n")
    
    # Shutdown if requested (only after ALL files are done)
    if shutdown_after and len(completed) > 0:
        print("⏻️  System shutting down in 60 seconds...")
        print("   (Run 'shutdown /a' to cancel)\n")
        os.system("shutdown /s /t 60")


# ========== GUI/CLI APPLICATION ==========

@Gooey(
    program_name="Anime Subber - AV1 Encoder & AI Subtitles",
    program_description="Convert anime videos to AV1 format with AI-generated English subtitles",
    default_size=(800, 700),
    navigation='SIDEBAR',
    sidebar_title='Configuration',
    richtext_controls=True,
    progress_regex=r"^frame=\s*(?P<current>\d+)",
    progress_expr="current / 100 * 100",
    timing_options={
        'show_time_remaining': True,
        'hide_time_remaining_on_complete': False,
    }
)
def main():
    """Main application entry point."""
    
    # Create parser
    parser = GooeyParser(
        description="Convert anime videos to AV1 format with AI-generated English subtitles"
    )
    
    # ========== INPUT GROUP (Mutually Exclusive) ==========
    input_group = parser.add_mutually_exclusive_group(required=True)
    
    # Build argument kwargs conditionally
    input_kwargs = {
        'metavar': 'Single Video File',
        'help': 'Select a single video file to process'
    }
    if GUI_MODE:
        input_kwargs['widget'] = 'FileChooser'
        input_kwargs['gooey_options'] = {
            'wildcard': "Video files (*.mp4;*.mkv;*.avi;*.mov)|*.mp4;*.mkv;*.avi;*.mov|All files (*.*)|*.*"
        }
    input_group.add_argument('--input', **input_kwargs)
    
    batch_kwargs = {
        'metavar': 'Batch Folder',
        'help': 'Select a folder to process all video files inside'
    }
    if GUI_MODE:
        batch_kwargs['widget'] = 'DirChooser'
    input_group.add_argument('--batch-folder', **batch_kwargs)
    
    # ========== HARDWARE & PERFORMANCE OPTIONS ==========
    hardware_group = parser.add_argument_group(
        'Hardware & Performance',
        'Configure encoding and AI processing settings'
    )
    
    device_kwargs = {
        'metavar': 'AI Device',
        'choices': ['cuda', 'cpu'],
        'default': 'cuda',
        'help': 'Device for Whisper AI inference (CUDA requires NVIDIA GPU)'
    }
    if GUI_MODE:
        device_kwargs['widget'] = 'Dropdown'
    hardware_group.add_argument('--device', **device_kwargs)
    
    resolution_kwargs = {
        'metavar': 'Target Resolution',
        'choices': ['source', '1440', '1080', '720'],
        'default': '1080',
        'help': 'Target video resolution (source = keep original)'
    }
    if GUI_MODE:
        resolution_kwargs['widget'] = 'Dropdown'
    hardware_group.add_argument('--resolution', **resolution_kwargs)
    
    preset_kwargs = {
        'metavar': 'SVT-AV1 Preset',
        'choices': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
        'default': '6',
        'help': 'Encoding preset: 0=slowest/best quality, 13=fastest/lower quality'
    }
    if GUI_MODE:
        preset_kwargs['widget'] = 'Dropdown'
    hardware_group.add_argument('--preset', **preset_kwargs)
    
    # ========== POST-TASK ACTION ==========
    action_group = parser.add_argument_group(
        'Post-Task Action',
        'What to do after processing completes'
    )
    
    shutdown_kwargs = {
        'action': 'store_true',
        'help': 'Shutdown the PC after ALL files are processed (60 second delay)'
    }
    if GUI_MODE:
        shutdown_kwargs['widget'] = 'CheckBox'
        shutdown_kwargs['metavar'] = 'Shutdown PC After Completion'
    action_group.add_argument('--shutdown', **shutdown_kwargs)
    
    # Parse arguments
    args = parser.parse_args()
    
    # ========== VALIDATE & PROCESS ==========
    
    # Determine input files
    if args.input:
        # Single file mode
        if not os.path.exists(args.input):
            print(f"❌ Error: File not found: {args.input}")
            sys.exit(1)
        
        files = [args.input]
        print(f"\n📁 Single File Mode")
        
    elif args.batch_folder:
        # Batch folder mode
        if not os.path.isdir(args.batch_folder):
            print(f"❌ Error: Folder not found: {args.batch_folder}")
            sys.exit(1)
        
        files = get_video_files_from_folder(args.batch_folder)
        
        if not files:
            print(f"❌ Error: No video files found in: {args.batch_folder}")
            print(f"   Supported formats: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}")
            sys.exit(1)
        
        print(f"\n📁 Batch Folder Mode")
        print(f"   Found {len(files)} video file(s)")
    
    else:
        print("❌ Error: Must specify either --input or --batch-folder")
        sys.exit(1)
    
    # Display configuration
    print(f"\n{'='*60}")
    print(f"⚙️  CONFIGURATION")
    print(f"{'='*60}")
    print(f"AI Device:       {args.device.upper()}")
    print(f"Resolution:      {args.resolution}p" if args.resolution != 'source' else f"Resolution:      Keep Original")
    print(f"SVT-AV1 Preset:  {args.preset} (0=slowest/best, 13=fastest)")
    print(f"Shutdown After:  {'Yes' if args.shutdown else 'No'}")
    print(f"{'='*60}\n")
    
    # Process files
    if len(files) == 1:
        # Single file processing
        output_file = process_single_file(
            files[0],
            args.device,
            args.resolution,
            args.preset
        )
        
        print(f"\n{'='*60}")
        print(f"✅ PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Final Output: {output_file}")
        print(f"{'='*60}\n")
        
        # Shutdown if requested
        if args.shutdown:
            print("⏻️  System shutting down in 60 seconds...")
            print("   (Run 'shutdown /a' to cancel)\n")
            os.system("shutdown /s /t 60")
    
    else:
        # Batch processing
        process_batch(
            files,
            args.device,
            args.resolution,
            args.preset,
            args.shutdown
        )


# ========== ENTRY POINT ==========

if __name__ == '__main__':
    main()
