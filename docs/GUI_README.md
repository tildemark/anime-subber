# Anime Subber - GUI Application 🎥 🖥️

A **hybrid GUI/CLI Windows Desktop Application** built with Gooey that converts anime videos to AV1 format and generates AI-translated English subtitles.

## ✨ Features

### 🎯 Hybrid Mode
- **GUI Mode**: Launch without arguments for a beautiful graphical interface
- **CLI Mode**: Pass arguments for command-line automation and scripting

### 📁 Flexible Input
- **Single File**: Process one video at a time
- **Batch Folder**: Automatically process all videos in a folder (*.mp4, *.mkv, *.avi, *.mov)

### ⚙️ Hardware Options
- **Device Selection**: Choose between CUDA (GPU) or CPU for Whisper AI
- **Resolution Control**: Source, 1440p, 1080p, or 720p
- **SVT-AV1 Preset**: 0-13 (0=slowest/best quality, 13=fastest)

### 🔧 Advanced Features
- **Post-Task Shutdown**: Automatically shutdown PC after ALL files complete
- **Low Priority Processing**: Keeps your system responsive during encoding
- **Progress Tracking**: Real-time status updates
- **Proper VAD Filtering**: Correctly escaped JSON parameters for Windows

---

## 📦 Installation

### 1. Install Dependencies

```powershell
# Install Gooey for GUI support
pip install gooey

# Install Whisper AI engine
pip install whisper-ctranslate2

# Install PyTorch with CUDA support (for NVIDIA GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 2. Verify FFmpeg

Ensure FFmpeg is installed and in your PATH:

```powershell
ffmpeg -version
```

If not installed, see the main [README.md](README.md) for installation instructions.

---

## 🚀 Usage

### GUI Mode (Recommended for Desktop Use)

Simply run without arguments:

```powershell
python main_app.py
```

Or double-click the script in Windows Explorer!

**GUI Features:**
- 📁 File/Folder chooser dialogs
- 🎛️ Dropdown menus for all options
- ✅ Checkbox for shutdown option
- 📊 Progress tracking
- 🎨 Modern dark theme interface

### CLI Mode (For Automation & Scripting)

Pass arguments for command-line operation:

```powershell
# Single file with CUDA
python main_app.py --input "movie.mp4" --device cuda --resolution 1080 --preset 6

# Batch folder with CPU
python main_app.py --batch-folder "C:\Videos\Anime" --device cpu --resolution 720 --preset 8

# With auto-shutdown after completion
python main_app.py --input "movie.mp4" --device cuda --shutdown
```

---

## 🎛️ Configuration Options

### Input (Mutually Exclusive)

| Option | Description | GUI Widget |
|--------|-------------|------------|
| `--input` | Single video file | FileChooser |
| `--batch-folder` | Folder containing videos | DirChooser |

### Hardware & Performance

| Option | Choices | Default | Description |
|--------|---------|---------|-------------|
| `--device` | cuda, cpu | cuda | Whisper AI device |
| `--resolution` | source, 1440, 1080, 720 | 1080 | Target resolution |
| `--preset` | 0-13 | 6 | SVT-AV1 preset (speed vs quality) |

### Post-Task Action

| Option | Description |
|--------|-------------|
| `--shutdown` | Shutdown PC after ALL files complete (60s delay) |

---

## 📊 Processing Pipeline

The application processes videos in **3 stages**:

### Stage 1: Video Encoding (CPU Intensive)
- Encodes video using **SVT-AV1** codec
- Converts audio to **Opus** @ 128kbps
- Runs at **low priority** to keep system responsive
- Applies anime-optimized tuning parameters

### Stage 2: AI Subtitle Generation (GPU/CPU)
- Uses **Whisper CTranslate2** for translation
- Translates Japanese audio → English subtitles
- **VAD filtering** skips silent segments
- Properly escaped JSON parameters for Windows compatibility

### Stage 3: Muxing (Fast)
- Combines video + subtitles into final MKV
- Preserves all streams without re-encoding
- Adds proper language metadata

---

## 📦 Creating a Standalone Executable

### Option 1: Basic Executable

```powershell
pyinstaller --onefile --windowed --name="AnimeSubber" main_app.py
```

### Option 2: With Custom Icon

First, create or download an icon file (`icon.ico`), then:

```powershell
pyinstaller --onefile --windowed --icon=icon.ico --name="AnimeSubber" main_app.py
```

### Option 3: Advanced (Recommended)

Create a `build_exe.ps1` script:

```powershell
# build_exe.ps1
pyinstaller `
    --onefile `
    --windowed `
    --icon=icon.ico `
    --name="AnimeSubber" `
    --add-data="README.md;." `
    --hidden-import=whisper_ctranslate2 `
    --hidden-import=torch `
    --clean `
    main_app.py

Write-Host "✅ Build complete! Executable: dist\AnimeSubber.exe"
```

Then run:

```powershell
.\build_exe.ps1
```

**Output**: `dist\AnimeSubber.exe` (standalone, no Python required!)

### Important Notes for Packaging

1. **FFmpeg**: The executable will look for `ffmpeg.exe` in the same folder, or use system PATH
2. **CUDA**: Users must have CUDA installed for GPU acceleration
3. **File Size**: Expect ~500MB due to PyTorch dependencies
4. **First Run**: May take longer as PyTorch initializes

---

## 🎯 Usage Examples

### Example 1: Single File (GUI)

1. Run `python main_app.py`
2. Click "Browse" next to "Single Video File"
3. Select your anime video
4. Choose settings:
   - Device: CUDA
   - Resolution: 1080
   - Preset: 6
5. Click "Start"

### Example 2: Batch Processing (GUI)

1. Run `python main_app.py`
2. Click "Browse" next to "Batch Folder"
3. Select folder containing multiple videos
4. Choose settings and enable "Shutdown PC After Completion"
5. Click "Start"
6. Go to bed - PC will shutdown when done! 😴

### Example 3: CLI Automation

```powershell
# Process all videos in a folder with optimal settings
python main_app.py `
    --batch-folder "D:\Anime\Season 1" `
    --device cuda `
    --resolution 1080 `
    --preset 6 `
    --shutdown
```

### Example 4: Quick Test (Low Quality)

```powershell
# Fast processing for testing
python main_app.py `
    --input "test.mp4" `
    --device cpu `
    --resolution 720 `
    --preset 13
```

---

## 🔧 Troubleshooting

### "No module named 'gooey'"

```powershell
pip install gooey
```

### "CUDA out of memory"

Switch to CPU mode:
- GUI: Select "cpu" from Device dropdown
- CLI: Add `--device cpu`

### "ffmpeg not found"

1. Install FFmpeg (see main README.md)
2. Or place `ffmpeg.exe` in the same folder as `main_app.py`

### GUI doesn't appear

Make sure you're running without arguments:

```powershell
# ✅ Correct (GUI mode)
python main_app.py

# ❌ Wrong (CLI mode)
python main_app.py --help
```

### Shutdown doesn't work

The shutdown command is:
```powershell
shutdown /s /t 60
```

To cancel:
```powershell
shutdown /a
```

---

## 📝 Technical Details

### VAD Filter Parameters

The application uses **properly escaped JSON** for Windows compatibility:

```python
vad_params = json.dumps({"min_silence_duration_ms": 500})
```

This prevents the common Windows error:
```
Error: unexpected character '{' in VAD parameters
```

### Low Priority Processing

All encoding operations use Windows low priority flag:

```python
subprocess.run(cmd, creationflags=0x00004000)
```

This keeps your system responsive during long encodes.

### Batch Processing Logic

- Processes files **sequentially** (one at a time)
- Shutdown only triggers after **ALL** files complete
- Failed files are tracked and reported
- Each file gets full 3-stage pipeline

---

## 🆚 Comparison: GUI vs CLI Scripts

| Feature | main_app.py (GUI) | pipeline_windows.py (CLI) |
|---------|-------------------|---------------------------|
| GUI Interface | ✅ Yes | ❌ No |
| CLI Support | ✅ Yes | ✅ Yes |
| Batch Folder | ✅ Auto-detect all videos | ❌ Requires wildcards |
| Device Selection | ✅ Dropdown | ❌ Hardcoded |
| Resolution Options | ✅ 4 choices | ⚠️ CLI argument only |
| Preset Options | ✅ 14 choices (0-13) | ⚠️ CLI argument only |
| Shutdown Management | ✅ Checkbox | ⚠️ CLI argument only |
| Standalone .exe | ✅ Yes (PyInstaller) | ❌ Requires Python |
| User-Friendly | ✅ Very | ⚠️ Technical users |

---

## 🎓 Advanced: Integrating with Existing Scripts

The `main_app.py` is designed to **coexist** with your existing scripts:

```
anime-subber/
├── main_app.py              # ⭐ NEW: GUI/CLI hybrid
├── scripts/
│   ├── pipeline_windows.py  # Original CLI pipeline
│   ├── encode_smart.py      # Original smart encoder
│   └── add_subtitles.py     # Original subtitle tool
└── wrappers/
    └── ps1/
        └── *.ps1            # Original PowerShell wrappers
```

**When to use each:**

- **main_app.py**: Desktop users, batch processing, visual interface
- **pipeline_windows.py**: Advanced users, custom scripting, automation
- **encode_smart.py**: Benchmarking, interactive quality selection
- **add_subtitles.py**: Subtitle-only processing

---

## 📞 Support

For issues specific to the GUI application:

1. Check this README first
2. Verify all dependencies are installed
3. Try CLI mode to isolate GUI issues
4. Check the main [README.md](README.md) for general troubleshooting

---

## 📄 License

MIT - Same as the main project

---

**Enjoy your new GUI! 🎉**

For the original CLI documentation, see [README.md](README.md)
