# Bundling Guide - Creating Standalone Executables

This guide explains how to create standalone `.exe` files with bundled dependencies (FFmpeg and Whisper models).

---

## 📦 Overview

You have **two bundling options**:

### Option 1: Basic Build (Smaller, Requires Internet)
- **Size**: ~500 MB
- **Includes**: Python, PyTorch, Gooey, Whisper
- **Requires**: FFmpeg in PATH or same folder
- **First Run**: Downloads Whisper models (~500 MB)
- **Use**: `build_exe.ps1`

### Option 2: Fully Bundled (Larger, Completely Offline)
- **Size**: ~1.5 GB
- **Includes**: Everything + FFmpeg + Whisper models
- **Requires**: Nothing! Completely standalone
- **First Run**: Works immediately offline
- **Use**: `build_exe_bundled.ps1`

---

## 🚀 Quick Start - Option 1 (Basic Build)

### Step 1: Install Dependencies

```powershell
pip install -r requirements_gui_pinned.txt
```

### Step 2: Build Executable

```powershell
.\build_exe.ps1
```

### Step 3: Distribute

```
YourApp/
├── AnimeSubber.exe     (from dist folder)
└── README.txt          (simple instructions)
```

**User Requirements**:
- FFmpeg in PATH (or provide ffmpeg.exe)
- Internet connection for first run (downloads Whisper model)
- NVIDIA drivers (for GPU mode)

---

## 🎯 Recommended - Option 2 (Fully Bundled)

### Step 1: Install Dependencies

```powershell
pip install -r requirements_gui_pinned.txt
```

### Step 2: Download FFmpeg

```powershell
.\download_ffmpeg.ps1
```

This downloads FFmpeg essentials (~80 MB) and extracts to `bundled/` folder.

### Step 3: Download Whisper Models (Optional)

```powershell
.\download_whisper_models.ps1
```

Choose which model to download:
- **tiny** (~75 MB) - Fastest, lowest quality
- **base** (~145 MB) - Fast, decent quality
- **small** (~488 MB) - **Recommended** - Balanced
- **medium** (~1.5 GB) - Slower, better quality
- **large** (~3 GB) - Slowest, best quality

**Recommendation**: Download `small` (the app's default)

### Step 4: Build Bundled Executable

```powershell
.\build_exe_bundled.ps1
```

The script will ask if you want to include Whisper models:
- **Yes**: Larger .exe (~1.5 GB), works completely offline
- **No**: Smaller .exe (~500 MB), downloads models on first run

### Step 5: Distribute

```
YourApp/
└── AnimeSubber.exe     (completely standalone!)
```

**User Requirements**:
- NVIDIA drivers (for GPU mode only)
- That's it! No Python, no FFmpeg, no internet needed!

---

## 📊 Size Comparison

| Build Type | .exe Size | Total Download | Offline? | User Setup |
|-----------|-----------|----------------|----------|------------|
| **Basic** | ~500 MB | ~500 MB | ❌ No | FFmpeg + Internet |
| **Bundled (no models)** | ~500 MB | ~580 MB | ⚠️ Partial | Internet (first run) |
| **Fully Bundled** | ~1.5 GB | ~1.5 GB | ✅ Yes | None! |

---

## 🛠️ Detailed Build Process

### Understanding the Bundled Folder

After running download scripts, you'll have:

```
anime-subber/
├── bundled/
│   ├── ffmpeg.exe          (~100 MB)
│   ├── ffprobe.exe         (~100 MB)
│   └── whisper-models/     (~500 MB, optional)
│       └── small/
│           ├── model.bin
│           ├── vocabulary.txt
│           └── ...
```

### How PyInstaller Bundles Files

The `build_exe_bundled.ps1` script uses:

```powershell
--add-data "bundled\ffmpeg.exe;."
--add-data "bundled\ffprobe.exe;."
--add-data "bundled\whisper-models;whisper-models"  # Optional
```

This tells PyInstaller to:
1. Include files in the executable
2. Extract them to a temp folder at runtime
3. The app finds them via `sys._MEIPASS`

### How the App Finds Bundled Files

The `main_app.py` has been updated with:

```python
def get_ffmpeg_path():
    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        bundled_ffmpeg = os.path.join(bundle_dir, "ffmpeg.exe")
        if os.path.exists(bundled_ffmpeg):
            return bundled_ffmpeg
    
    # Fall back to script directory or PATH
    ...
```

This automatically detects bundled FFmpeg!

---

## 🔧 Advanced Customization

### Custom Icon

1. Create or download an `.ico` file
2. Place it in the project root as `icon.ico`
3. The build scripts will automatically use it

### Bundling Specific Whisper Model

Edit `build_exe_bundled.ps1` to bundle a specific model:

```powershell
# Only bundle 'tiny' model (smaller .exe)
--add-data "bundled\whisper-models\tiny;whisper-models\tiny"
```

### Excluding Unnecessary Files

Create a custom `.spec` file for fine-grained control:

```powershell
# Generate spec file
pyinstaller --onefile main_app.py

# Edit AnimeSubber.spec to customize
notepad AnimeSubber.spec

# Build from spec
pyinstaller AnimeSubber.spec
```

---

## 📝 Distribution Best Practices

### For End Users (Non-Technical)

**Fully Bundled Build** (Option 2 with models):

```
AnimeSubber_v1.0/
├── AnimeSubber.exe
├── README.txt
└── LICENSE.txt
```

**README.txt** should include:
- Double-click to run
- Select file or folder
- Choose settings
- Click Start
- (Optional) NVIDIA GPU recommended

### For Power Users

**Basic Build** (Option 1):

```
AnimeSubber_v1.0/
├── AnimeSubber.exe
├── ffmpeg.exe (optional)
├── README.txt
└── ADVANCED.txt
```

**ADVANCED.txt** should include:
- CLI usage examples
- FFmpeg installation instructions
- GPU vs CPU mode explanation
- Troubleshooting tips

### For Developers

Provide source code + build instructions:

```
AnimeSubber_Source/
├── main_app.py
├── requirements_gui_pinned.txt
├── build_exe_bundled.ps1
├── download_ffmpeg.ps1
├── download_whisper_models.ps1
└── BUILD_INSTRUCTIONS.md
```

---

## ⚠️ Common Issues

### "FFmpeg not found" in bundled .exe

**Cause**: FFmpeg wasn't included in build

**Solution**:
1. Verify `bundled/ffmpeg.exe` exists
2. Re-run `.\download_ffmpeg.ps1`
3. Re-build with `.\build_exe_bundled.ps1`

### .exe is too large (>2 GB)

**Cause**: Bundled too many Whisper models

**Solution**:
- Only bundle `small` model (not all models)
- Or don't bundle models (download on first run)

### "CUDA out of memory" on user's PC

**Cause**: User's GPU has less VRAM than yours

**Solution**:
- App automatically falls back to CPU if CUDA fails
- Or provide CPU-only build (smaller, no CUDA)

### Antivirus flags the .exe

**Cause**: PyInstaller executables sometimes trigger false positives

**Solution**:
- Code sign the executable (requires certificate)
- Provide source code for verification
- Submit to antivirus vendors for whitelisting

---

## 🎓 Build Strategies

### Strategy 1: Single Universal Build

**Pros**:
- One .exe for everyone
- Simplest distribution

**Cons**:
- Large file size (~1.5 GB)
- Long download time

**Best for**: Small user base, offline usage

### Strategy 2: Two Builds (GPU + CPU)

**GPU Build**:
- Includes CUDA PyTorch (~1.5 GB)
- For users with NVIDIA GPUs

**CPU Build**:
- CPU-only PyTorch (~500 MB)
- For users without GPUs

**Best for**: Large user base, optimize download size

### Strategy 3: Installer Package

Use a tool like **Inno Setup** or **NSIS** to create an installer:

```
AnimeSubber_Setup.exe
├── Installs to Program Files
├── Creates desktop shortcut
├── Downloads models on first run
└── Adds to Start Menu
```

**Best for**: Professional distribution

---

## 📦 Creating an Installer (Advanced)

### Using Inno Setup

1. Download Inno Setup: https://jrsoftware.org/isinfo.php

2. Create `installer.iss`:

```ini
[Setup]
AppName=Anime Subber
AppVersion=1.0
DefaultDirName={pf}\AnimeSubber
DefaultGroupName=Anime Subber
OutputDir=installer
OutputBaseFilename=AnimeSubber_Setup

[Files]
Source: "dist\AnimeSubber.exe"; DestDir: "{app}"
Source: "bundled\ffmpeg.exe"; DestDir: "{app}"
Source: "bundled\ffprobe.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Anime Subber"; Filename: "{app}\AnimeSubber.exe"
Name: "{commondesktop}\Anime Subber"; Filename: "{app}\AnimeSubber.exe"
```

3. Compile with Inno Setup

4. Distribute `AnimeSubber_Setup.exe`

---

## 🔍 Testing Your Build

### Test Checklist

- [ ] .exe runs without errors
- [ ] GUI appears correctly
- [ ] File chooser works
- [ ] Folder chooser works
- [ ] FFmpeg is found (no "not found" errors)
- [ ] Whisper models download or are bundled
- [ ] Video encoding works
- [ ] Subtitle generation works
- [ ] Final output is created
- [ ] Shutdown option works (test carefully!)

### Test on Clean System

**Important**: Test on a PC without Python/FFmpeg installed!

1. Use a VM or friend's PC
2. Copy only the .exe
3. Try to process a short video
4. Verify it works completely standalone

---

## 📊 Build Comparison Matrix

| Feature | build_exe.ps1 | build_exe_bundled.ps1 |
|---------|---------------|----------------------|
| **FFmpeg Bundled** | ❌ No | ✅ Yes |
| **Whisper Bundled** | ❌ No | ⚠️ Optional |
| **.exe Size** | ~500 MB | ~500 MB - 1.5 GB |
| **User Needs FFmpeg** | ✅ Yes | ❌ No |
| **User Needs Internet** | ✅ Yes (first run) | ⚠️ Optional |
| **Build Time** | ~5 min | ~5-10 min |
| **Download Scripts** | Not needed | Required |
| **Best For** | Developers | End users |

---

## 🎯 Recommendations

### For Personal Use
→ Use **build_exe.ps1** (basic build)
- Faster to build
- You already have FFmpeg

### For Sharing with Friends
→ Use **build_exe_bundled.ps1** without models
- No FFmpeg setup needed
- Models download automatically

### For Public Distribution
→ Use **build_exe_bundled.ps1** with models
- Completely standalone
- Works offline
- Best user experience

---

## 📞 Need Help?

- **Build fails**: Check `test_installation.ps1` first
- **Missing FFmpeg**: Run `download_ffmpeg.ps1`
- **Large .exe**: Don't bundle models, or use compression
- **Slow build**: Normal for PyInstaller with PyTorch

---

**Last Updated**: 2026-02-05
