# 🚀 Quick Start Guide - AnimeSubber GUI

This guide will get you up and running with the GUI application in **5 minutes**.

---

## ⚡ Super Quick Start (3 Steps)

### 1️⃣ Install Dependencies

```powershell
# Install all required packages
pip install -r requirements_gui.txt
```

### 2️⃣ Launch the GUI

```powershell
# Run the application
python main_app.py
```

### 3️⃣ Process Your First Video

1. Click **"Browse"** next to "Single Video File"
2. Select your anime video (MP4, MKV, etc.)
3. Choose your settings:
   - **Device**: CUDA (if you have NVIDIA GPU) or CPU
   - **Resolution**: 1080 (recommended)
   - **Preset**: 6 (balanced quality/speed)
4. Click **"Start"**
5. ☕ Grab a coffee - this will take a while!

---

## 📋 Detailed Setup

### Step 1: Verify FFmpeg

```powershell
# Check if FFmpeg is installed
ffmpeg -version
```

**If not installed**, download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to PATH.

### Step 2: Install Python Packages

```powershell
# Option A: Use requirements file (recommended)
pip install -r requirements_gui.txt

# Option B: Manual installation
pip install gooey
pip install whisper-ctranslate2
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Step 3: Test Installation

```powershell
# Verify dependencies
python scripts/check_dependencies.py
```

You should see:
- ✅ FFmpeg found
- ✅ Python 3.8+
- ✅ whisper-ctranslate2 installed
- ✅ CUDA available (if you have NVIDIA GPU)

---

## 🎯 Usage Scenarios

### Scenario 1: Single Movie

**Goal**: Convert one anime movie with best quality

1. Run: `python main_app.py`
2. Select your movie file
3. Settings:
   - Device: **CUDA**
   - Resolution: **source** (keep original)
   - Preset: **6** (best quality)
4. Start processing
5. Output: `movie_final.mkv` with embedded English subtitles

**Time**: ~40-80 hours for a 2-hour movie (depends on hardware)

---

### Scenario 2: Batch Processing

**Goal**: Convert entire anime season overnight

1. Run: `python main_app.py`
2. Select **"Batch Folder"** instead of single file
3. Choose folder containing all episodes
4. Settings:
   - Device: **CUDA**
   - Resolution: **1080**
   - Preset: **8** (faster)
   - ✅ **Enable "Shutdown PC After Completion"**
5. Start processing
6. Go to bed 😴

**Result**: All episodes converted + PC shuts down automatically

---

### Scenario 3: Quick Test

**Goal**: Test the application quickly

1. Run: `python main_app.py`
2. Select a short video clip (1-5 minutes)
3. Settings:
   - Device: **CPU** (no GPU needed for testing)
   - Resolution: **720**
   - Preset: **13** (fastest)
4. Start processing

**Time**: ~10-30 minutes for a 5-minute clip

---

## 🔧 Common Settings Explained

### Device

| Option | When to Use | Speed | Requirements |
|--------|-------------|-------|--------------|
| **CUDA** | You have NVIDIA GPU | ⚡⚡⚡ Fast | NVIDIA GPU + CUDA drivers |
| **CPU** | No GPU or testing | 🐌 Slow | Any CPU |

### Resolution

| Option | Description | File Size | Quality |
|--------|-------------|-----------|---------|
| **source** | Keep original resolution | Largest | Best |
| **1440** | Downscale to 1440p | Medium | Excellent |
| **1080** | Downscale to 1080p | Medium | Great |
| **720** | Downscale to 720p | Smallest | Good |

### SVT-AV1 Preset

| Preset | Speed | Quality | Use Case |
|--------|-------|---------|----------|
| **0-3** | 🐌 Very Slow | ⭐⭐⭐⭐⭐ | Archival quality |
| **4-6** | 🐌 Slow | ⭐⭐⭐⭐ | **Recommended** |
| **7-9** | ⚡ Medium | ⭐⭐⭐ | Balanced |
| **10-13** | ⚡⚡⚡ Fast | ⭐⭐ | Quick tests |

---

## 📦 Creating a Standalone .exe

Want to share with friends who don't have Python?

### Option 1: Use Build Script (Easiest)

```powershell
# Run the automated build script
.\build_exe.ps1
```

Output: `dist\AnimeSubber.exe` (ready to share!)

### Option 2: Manual PyInstaller

```powershell
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name="AnimeSubber" main_app.py
```

### Distributing the .exe

**What to include:**
1. `AnimeSubber.exe` (from `dist\` folder)
2. `ffmpeg.exe` (optional, if user doesn't have it in PATH)
3. Short README with instructions

**What users need:**
- Windows 10/11
- NVIDIA GPU + CUDA drivers (for GPU mode)
- That's it! No Python required.

---

## ❓ Troubleshooting

### "No module named 'gooey'"

```powershell
pip install gooey
```

### "CUDA out of memory"

**Solution 1**: Use CPU mode
- GUI: Select "cpu" from dropdown
- CLI: Add `--device cpu`

**Solution 2**: Close other GPU applications
- Close games, browsers, etc.
- Check Task Manager → Performance → GPU

### "ffmpeg not found"

**Solution 1**: Install FFmpeg system-wide
- Download: https://www.gyan.dev/ffmpeg/builds/
- Add to PATH

**Solution 2**: Use local FFmpeg
- Place `ffmpeg.exe` in same folder as `main_app.py`

### GUI doesn't appear

Make sure you're running **without** arguments:

```powershell
# ✅ Correct (GUI mode)
python main_app.py

# ❌ Wrong (CLI mode)
python main_app.py --input movie.mp4
```

### Processing is very slow

**Check:**
1. Are you using CPU mode? (CUDA is much faster)
2. Is your preset too low? (Try 8 or 10 instead of 6)
3. Is your resolution too high? (Try 720p instead of source)

**Typical speeds (Ryzen 2600 + GTX 1050):**
- Video encoding: 0.5-2 fps (normal, very slow)
- Subtitle generation: 5-10x realtime (fast)

---

## 🎓 Next Steps

1. ✅ **Complete this quick start**
2. 📖 **Read [GUI_README.md](GUI_README.md)** for detailed documentation
3. 🔧 **Experiment with settings** on short clips
4. 🚀 **Process your anime collection**
5. 📦 **Build .exe** to share with friends

---

## 📞 Need Help?

1. Check [GUI_README.md](GUI_README.md) for detailed docs
2. Check [README.md](README.md) for general troubleshooting
3. Verify dependencies: `python scripts/check_dependencies.py`

---

**Happy encoding! 🎉**
