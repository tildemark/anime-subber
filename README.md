# Anime AV1 Subber 🎥 🤖

An automated Python pipeline to convert high-resolution Japanese anime into efficient **AV1** format and generate **AI-translated English subtitles** locally.

This project is specifically optimized for mid-range hardware (tested on **Ryzen 2600** and **NVIDIA GTX 1050 2GB VRAM**) to handle long-form movies without system lag or memory crashes.

## 🌟 Features
- **Modern Compression:** Uses `SVT-AV1` for superior quality-to-size ratio.
- **GPU Option (encode_smart):** Optional HEVC NVENC path for faster encodes on NVIDIA GPUs.
- **AI Translation:** Leverages `Whisper-CTranslate2` to turn Japanese audio into English `.srt` files.
- **VAD Integration:** Voice Activity Detection skips silent/action scenes to prevent AI hallucinations.
- **Resource Friendly:** Runs with low-priority flags to keep your OS responsive.
- **Automated Muxing:** Automatically packages video and subtitles into a single `.mkv` container.
- **Batch Processing:** Use wildcards to process multiple files at once.
- **Easy-to-Use Wrappers:** Shell scripts (`.sh` for Linux/macOS) and PowerShell scripts (`.ps1` for Windows) for simplified execution.

---

## 🚀 Quick Start (Easiest Way)

**Windows PowerShell:**
```powershell
.\wrappers\ps1\pipeline_windows.ps1 movie.mp4
```

**Linux/macOS Terminal:**
```bash
chmod +x wrappers/sh/*.sh  # Make scripts executable (first time only)
./wrappers/sh/pipeline_unix.sh movie.mp4
```

These wrapper scripts handle everything - no need to type `python` commands!

---

## � Project Structure

```
anime-subber/
├── scripts/                    # Python scripts (core logic)
│   ├── pipeline_windows.py     # Full pipeline (Windows)
│   ├── pipeline_unix.py        # Full pipeline (Linux/macOS)
│   ├── encode_smart.py         # Smart AV1 encoding with benchmarking
│   ├── encode_simple.py        # Basic AV1 encoding
│   ├── add_subtitles.py        # AI subtitle generation & muxing
│   ├── benchmark.py            # Hardware performance testing
│   ├── bench_encoding.py       # Encoding speed benchmark
│   └── check_dependencies.py   # ⭐ Dependency verification tool
│
├── wrappers/                   # Convenient wrapper scripts
│   ├── ps1/                    # PowerShell scripts (Windows)
│   │   ├── pipeline_windows.ps1
│   │   ├── pipeline_unix.ps1
│   │   ├── encode_smart.ps1
│   │   ├── encode_simple.ps1
│   │   ├── add_subtitles.ps1
│   │   ├── benchmark.ps1
│   │   ├── bench_encoding.ps1
│   │   └── check_dependencies.ps1
│   │
│   └── sh/                     # Shell scripts (Linux/macOS)
│       ├── pipeline_windows.sh
│       ├── pipeline_unix.sh
│       ├── encode_smart.sh
│       ├── encode_simple.sh
│       ├── add_subtitles.sh
│       ├── benchmark.sh
│       ├── bench_encoding.sh
│       └── check_dependencies.sh
│
├── docs/                       # Additional documentation
│   └── VISUAL_OVERVIEW.md      # Flowcharts & diagrams
│
├── README.md                   # This file (main documentation)
└── CHANGELOG.md                # Version history
```

**Why organize this way?**

This structure solves real problems that existed when all 25+ files were in the root directory:

1. **Easier Navigation** - Before: scroll through 25 files. After: 4 clear folders (scripts, wrappers, docs, root docs)

2. **Clearer Purpose** - New users instantly understand:
   - `scripts/` = The actual programs
   - `wrappers/` = Convenient shortcuts grouped by OS
   - `docs/` = Extra documentation

3. **Better Version Control** - Git diffs are cleaner when files are grouped by purpose

4. **Simpler Onboarding** - New contributors don't need to guess what `convert2.py` does when it's clearly named `encode_smart.py` in a `scripts/` folder

5. **Cross-Platform Clarity** - Windows users know to look in `wrappers/ps1/`, Linux users in `wrappers/sh/`. No confusion about which file to run.

6. **GitHub Best Practice** - README.md in root automatically displays on the repository homepage

7. **Scalability** - Adding new scripts or wrappers doesn't clutter the root. Everything has a logical home.

**Real-world benefit:** Instead of seeing a wall of 25 files, you now see 4 folders + 2 docs. Finding what you need takes seconds instead of minutes.

---

## �🛠️ Prerequisites

### 1. FFmpeg Installation

FFmpeg is required for video encoding and muxing.

> **Optional:** If you place a local `ffmpeg.exe` alongside the scripts, the encoders will use it automatically (Windows only). Put it in `scripts/ffmpeg.exe`.

#### **Windows Installation:**

1. **Download FFmpeg:**
   - Visit [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
   - Download the **"ffmpeg-release-essentials.zip"** (around 80MB)

2. **Extract to a permanent location:**
   ```
   Recommended: C:\ffmpeg\
   ```
   After extraction, you should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add FFmpeg to System PATH:**
   
   **Method 1: Using Windows Settings (Recommended)**
   - Press `Win + X` and select **"System"**
   - Click **"Advanced system settings"** on the right
   - Click **"Environment Variables"** button
   - Under **"System variables"**, find and select **"Path"**
   - Click **"Edit"** → **"New"**
   - Add: `C:\ffmpeg\bin` (or wherever you extracted it)
   - Click **"OK"** on all windows
   - **Restart your terminal/PowerShell**

   **Method 2: Using PowerShell (Quick)**
   ```powershell
   # Run PowerShell as Administrator
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "Machine")
   ```

4. **Verify Installation:**
   ```powershell
   # Close and reopen PowerShell, then run:
   ffmpeg -version
   ```
   You should see FFmpeg version information.

#### **Linux Installation:**
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# Verify
ffmpeg -version
```

#### **macOS Installation:**
```bash
# Using Homebrew (install brew first if needed: https://brew.sh)
brew install ffmpeg

# Verify
ffmpeg -version
```

### 2. Python Dependencies

Ensure you have Python 3.8+ installed. It is highly recommended to use a GPU with CUDA support.

```bash
# Install the optimized Whisper engine
pip install whisper-ctranslate2

# Install Torch with CUDA support (for NVIDIA GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 3. Verify All Dependencies

Run the dependency checker to ensure everything is properly installed:

```bash
# Using wrapper (recommended)
.\wrappers\ps1\check_dependencies.ps1   # Windows
./wrappers/sh/check_dependencies.sh     # Linux/macOS

# Or direct Python
python scripts/check_dependencies.py
```

This will verify:
- ✅ FFmpeg installation and PATH configuration
- ✅ Python version (3.8+)
- ✅ Required Python packages (whisper-ctranslate2, torch)
- ✅ CUDA availability for GPU acceleration

---

## 🚀 Quick Start

### 1. Single File Conversion

**Using Wrapper Scripts (Recommended):**
```bash
# From the project directory:
# Windows PowerShell
.\wrappers\ps1\pipeline_windows.ps1 movie.mp4

# Linux/macOS Shell
./wrappers/sh/pipeline_unix.sh movie.mp4
./wrappers/sh/encode_smart.sh movie.mp4
./wrappers/sh/add_subtitles.sh encoded.mkv

# From your video folder (use full path to script):
# Windows
C:\code\anime-subber\wrappers\ps1\pipeline_windows.ps1 movie.mp4

# Linux/macOS
/home/user/anime-subber/wrappers/sh/pipeline_unix.sh movie.mp4
```

**Direct Python:**
```bash
# Windows - Video + Subtitles
python scripts/pipeline_windows.py movie.mp4 output.mkv

# Linux/macOS - Video + Subtitles
python scripts/pipeline_unix.py movie.mp4 output.mkv

# Video Only (with smart benchmarking)
python scripts/encode_smart.py movie.mp4 output.mkv

# Subtitles Only (for existing encoded video)
python scripts/add_subtitles.py encoded.mkv final.mkv
```

### 2. Batch Conversion (Wildcard)

**Using Wrapper Scripts (Recommended):**
```bash
# Windows PowerShell
.\wrappers\ps1\pipeline_windows.ps1 "*.mp4"
.\wrappers\ps1\encode_smart.ps1 "season1/*.mkv"

# Linux/macOS Shell
./wrappers/sh/pipeline_unix.sh "*.mp4"
./wrappers/sh/encode_smart.sh "season1/*.mkv"
```

**Direct Python:**
```bash
# Convert all MP4 files in current directory
python scripts/pipeline_windows.py "*.mp4"

# Convert all MKV files
python scripts/encode_smart.py "*.mkv"

# Convert files from subdirectory
python pipeline_windows.py "./videos/*.mp4"
```

---

## � Running Scripts From Any Folder

**If you're in a folder with your MP4 videos** (not in the project directory):

### **Windows PowerShell:**
```powershell
# Option 1: Use absolute path to wrapper script
C:\code\anime-subber\wrappers\ps1\pipeline_windows.ps1 movie.mp4

# Option 2: Use relative path (if you know where project is)
..\..\anime-subber\wrappers\ps1\pipeline_windows.ps1 *.mp4

# Option 3: Add project to PATH (one-time setup)
# Add C:\code\anime-subber\wrappers\ps1 to your PATH
# Then from any folder:
pipeline_windows.ps1 movie.mp4
```

### **Linux/macOS:**
```bash
# Option 1: Use absolute path
/home/user/anime-subber/wrappers/sh/pipeline_unix.sh movie.mp4

# Option 2: Use relative path
../../anime-subber/wrappers/sh/pipeline_unix.sh *.mp4

# Option 3: Create symlink (one-time setup)
sudo ln -s /home/user/anime-subber/wrappers/sh/pipeline_unix.sh /usr/local/bin/anime-subber
# Then from any folder:
anime-subber movie.mp4
```

### **Direct Python (All Platforms):**
```bash
# Use absolute path to Python script
python C:\code\anime-subber\scripts\pipeline_windows.py movie.mp4

# Or navigate to project first, then specify video location
cd C:\code\anime-subber
python scripts\pipeline_windows.py "C:\Videos\movie.mp4"
```

**💡 Pro Tip:** For frequent use, create a shortcut/alias pointing to the wrapper scripts so you can run them from anywhere without typing full paths.

---

## �📋 Script Comparison

| Script | Purpose | Best For | Time |
|--------|---------|----------|------|
| **scripts/pipeline_windows.py** | Video + Subtitles | Windows, full pipeline | 40-80h |
| **scripts/pipeline_unix.py** | Video + Subtitles | Linux/macOS, full pipeline | 40-80h |
| **scripts/encode_smart.py** | Video only, smart | Video-only with benchmarking | 40-80h |
| **scripts/encode_simple.py** | Video only, basic | Quick video encoding | 40-80h |
| **scripts/add_subtitles.py** | Subtitles only | Existing encoded videos | ~30min |
| **scripts/benchmark.py** | Benchmark only | Test hardware speeds | ~2min |
| **scripts/check_dependencies.py** | Setup verification | Check all requirements | ~5sec |

---

## 🎯 Which Script Should I Use?

### ✅ Best Choice: Everything in One Command
```bash
python scripts/pipeline_windows.py input.mp4 output.mkv
```
→ Encodes video + generates subtitles + combines them
→ Takes: 40-80 hours total (90% video, 10% subs)

### ✅ If You Only Want Video
```bash
python scripts/encode_smart.py input.mp4 output.mkv
```
→ Smart benchmarking first, then you pick settings (CPU SVT-AV1 or GPU NVENC)
→ Takes: 40-80 hours

### ✅ If You Already Have Encoded Video
```bash
python scripts/add_subtitles.py encoded.mkv final.mkv
```
→ Just adds subtitles, no re-encoding
→ Takes: ~30 minutes

### ✅ Batch Processing
```bash
python scripts/pipeline_windows.py "*.mp4"
```
→ Processes all MP4 files in directory sequentially
→ Perfect for converting multiple episodes

**encode_smart batch mode** benchmarks the first file, then applies your chosen option to the rest.

---

## ⚙️ Configuration

### Resolution Options
- `source` - Keep original resolution (best quality)
- `720` - Downscale to 720p (smaller file)
- `1080` - Downscale to 1080p

### Preset Levels (Speed vs Quality)
- `6` - Slow, best quality (~68 hours for 2h video on Ryzen 2600)
- `8` - Balanced (~45 hours)
- `10` - Fast (~19 hours)

### CRF Quality
- `30` - Default, good quality (~17% file retention)
- `36` - More compression (~25% file size)
- `40` - Very compressed (~35% file size)

### Windows Auto-Shutdown
```bash
python scripts/pipeline_windows.py input.mp4 output.mkv source 6 30 y
#                                                            ^ auto-shutdown when done
```

---

## 📊 Performance Benchmarks (Ryzen 2600)

For a 2-hour anime video:

| Preset | Resolution | Time | File Size | Quality |
|--------|-----------|------|-----------|---------|
| P6/CRF30 | 1080p | 68h | 1.2GB | ⭐⭐⭐⭐⭐ |
| P8/CRF36 | 1080p | 45h | 1.5GB | ⭐⭐⭐⭐☆ |
| P8/CRF32 | 720p | 32h | 0.8GB | ⭐⭐⭐⭐☆ |
| P10/CRF40 | 720p | 19h | 0.6GB | ⭐⭐⭐☆☆ |

**Source: 5.8GB → Output: 1.0GB (85% reduction)**

---

## 📁 File Outputs

### Using scripts/pipeline_windows.py or scripts/pipeline_unix.py:
```
Created files:
├── output.mkv         (intermediate - encoded video)
├── input_base.srt     (intermediate - subtitles)
└── output_final.mkv   (FINAL - video with embedded subtitles)
```
*You can delete the first two files after completion*

### Using encode_smart.py:
```
Created files:
└── output.mkv         (FINAL - encoded video, no subtitles)
```

### Using add_subtitles.py:
```
Created files:
├── input_base.srt     (intermediate - subtitles)
└── output.mkv         (FINAL - video with embedded subtitles)
```

---

## 🐛 Troubleshooting

### "How long will this take?"
→ Run `python scripts/benchmark.py input.mp4` (takes ~2 minutes to estimate)

### "Whisper process failed"
→ Check if other apps are using GPU VRAM
→ Try reducing `--beam_size` in add_subtitles.py

### "ffmpeg not found"
→ Ensure ffmpeg is in your system PATH
→ Run `ffmpeg -version` to verify installation

### "CUDA out of memory"
→ Try running only one conversion at a time
→ Use lower preset (8-10 instead of 6)

---

## 🎓 Understanding the Code

All Python files include:
- **Docstrings** at the top explaining purpose
- **Section headers** (========) for easy navigation
- **Inline comments** explaining complex logic
- **Parameter documentation** in functions
- **Clear status messages** during execution

Example:
```python
"""
Script Name: pipeline_windows.py
Purpose: Complete video + subtitle pipeline
Usage: python pipeline_windows.py input.mp4 output.mkv [args]
"""

# ========== STAGE 1: VIDEO ENCODING ==========
# Explanation of what happens here...
```

---

## 📊 Batch Processing Examples

### Convert All Episodes in a Folder
```bash
# All MP4 files
python scripts/pipeline_windows.py "season1/*.mp4"

# Process with custom settings (if supported by script)
python scripts/encode_smart.py "anime_*.mkv"
```

### Advanced: Process with Patterns
```bash
# All video files
python scripts/pipeline_unix.py "*.{mp4,mkv}"

# Specific naming pattern
python scripts/add_subtitles.py "episode_*.mp4"
```

---

## 🛠️ Advanced Usage

### Windows with Auto-Shutdown
```bash
# Shutdown PC when all conversions complete
python scripts/pipeline_windows.py input.mp4 output.mkv source 6 30 y
```

### Custom Quality Settings
```bash
# Fast encode (Preset 10, CRF 40)
python scripts/pipeline_windows.py input.mp4 output.mkv 720 10 40

# High quality (Preset 6, CRF 30)
python scripts/pipeline_windows.py input.mp4 output.mkv source 6 30
```

### Testing Your Hardware
```bash
# Benchmark 4 preset options
python scripts/benchmark.py input.mp4

# Then use best option with encode_smart.py
python scripts/encode_smart.py input.mp4 output.mkv
```

---

## 📝 Output Container Info

All outputs are **MKV** (Matroska) format with:
- **Video Codec:** AV1 (libsvtav1)
- **Audio Codec:** Opus @ 128kbps
- **Subtitles:** SRT format (if using full pipeline)
- **Language Tags:** Automatically set to English for subtitles

---

## 🚀 Next Steps

1. **Install FFmpeg** (see Prerequisites section above for detailed instructions)
2. **Install Python dependencies:**
   ```bash
   pip install whisper-ctranslate2
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```
3. **Verify your setup:**
   ```bash
   .\wrappers\ps1\check_dependencies.ps1    # Windows
   ./wrappers/sh/check_dependencies.sh      # Linux/macOS
   ```
4. **Choose your script** based on needs (see Script Comparison above)
5. **Run your first conversion:**
   ```bash
   .\wrappers\ps1\pipeline_windows.ps1 movie.mp4    # Windows
   ./wrappers/sh/pipeline_unix.sh movie.mp4         # Linux/macOS
   ```
6. **Monitor progress** with clear status messages throughout encoding

---

## 📞 Questions?

- **Which script to use?** See "Script Comparison" section above
- **How long will it take?** Use `scripts/benchmark.py` to test on your hardware
- **How do I batch process?** Use wildcard patterns (see "Batch Processing" section)
- **What are these settings?** See "Configuration" section
- **Why is it slow?** Check "Performance Benchmarks" for expected times on your hardware

See [CHANGELOG.md](CHANGELOG.md) for version history.
See [VISUAL_OVERVIEW.md](docs/VISUAL_OVERVIEW.md) for flowcharts and diagrams.

**Downscale to 1440p and subtitle:**

```bash
python scripts/pipeline_windows.py raw_4k_source.mp4 movie_1440p.mkv 1440

```

## 🏗️ How it Works

The pipeline runs in three distinct stages:

1. **Stage 1 (CPU):** Encodes video to AV1 and audio to Opus. Using a low-priority flag allows the Ryzen 2600 to handle the heavy encoding without freezing your PC.
2. **Stage 2 (GPU):** Runs the `small` Whisper model with `int8` quantization. This fits the model entirely within **2GB of VRAM**, ensuring speed and stability.
3. **Stage 3 (Mux):** Uses FFmpeg to "remux" the new video and the AI-generated `.srt` into a final `.mkv` with proper metadata.

## ⚙️ Configuration for Low VRAM

If you have exactly 2GB of VRAM, the script is pre-configured with:

* `--model small`: The best accuracy-to-memory ratio.
* `--compute_type int8`: Reduces memory footprint significantly.
* `--vad_filter True`: Skips non-speech segments to save processing time.

## 📄 License

MIT

---

Maintainer: [tildemark](https://www.google.com/search?q=https://github.com/tildemark) | Website: [sanchez.ph](https://sanchez.ph)

```
