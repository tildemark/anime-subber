# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

## ❌ "ModuleNotFoundError: No module named 'six'"

### Problem
```
ModuleNotFoundError: No module named 'six'
```

### Solution
The `six` package is required by Gooey but sometimes doesn't install automatically.

```powershell
# Quick fix
pip install six

# If that doesn't work, force reinstall
pip install --force-reinstall --no-cache-dir six

# Or reinstall all requirements
pip install -r requirements_gui_pinned.txt
```

---

## ❌ "AttributeError: 'function' object has no attribute 'ESC'"

### Problem
```
AttributeError: 'function' object has no attribute 'ESC'
```

### Solution
This is caused by `colored` package version 2.x which breaks Gooey compatibility.

```powershell
# Downgrade to compatible version
pip install colored==1.4.4

# Force reinstall if needed
pip install --force-reinstall --no-cache-dir colored==1.4.4
```

---

## ❌ "FFmpeg not found"

### Problem
```
'ffmpeg' is not recognized as an internal or external command
```

### Solutions

#### Option 1: Install FFmpeg System-Wide
1. Download FFmpeg: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add `C:\ffmpeg\bin`
   - Restart terminal

#### Option 2: Use Local FFmpeg
```powershell
# Place ffmpeg.exe in project folder
copy "C:\path\to\ffmpeg.exe" "C:\code\anime-subber\"
```

#### Option 3: Bundle with .exe
```powershell
.\download_ffmpeg.ps1
.\build_exe_bundled.ps1
```

---

## ❌ GUI Doesn't Open

### Problem
Running `python main_app.py` shows error or nothing happens.

### Solutions

#### Check 1: Are you passing arguments?
```powershell
# This opens GUI (no arguments)
python main_app.py

# This uses CLI mode (has arguments)
python main_app.py --help
```

#### Check 2: Verify Gooey is installed
```powershell
pip show gooey
```

If not installed:
```powershell
pip install gooey
```

#### Check 3: Check for errors
```powershell
# Run with verbose output
python -v main_app.py
```

---

## ❌ "CUDA out of memory"

### Problem
```
RuntimeError: CUDA out of memory
```

### Solutions

#### Option 1: Use CPU mode
```powershell
# GUI: Select "cpu" from device dropdown
# CLI: Add --device cpu
python main_app.py --input "video.mp4" --device cpu
```

#### Option 2: Close other GPU applications
- Close games, video editors, browsers with hardware acceleration
- Check Task Manager → Performance → GPU

#### Option 3: Use smaller model
Edit `main_app.py` line 163:
```python
"--model", "tiny",  # Change from "small" to "tiny"
```

---

## ❌ Whisper Model Download Fails

### Problem
```
Failed to download model
```

### Solutions

#### Option 1: Manual download
```powershell
.\download_whisper_models.ps1
```

#### Option 2: Check internet connection
- Verify internet is working
- Check firewall/antivirus settings
- Try different network

#### Option 3: Use different model
```powershell
# Download smaller model first
python -c "from whisper_ctranslate2 import download_model; download_model('tiny')"
```

---

## ❌ "No video files found"

### Problem
```
Error: No video files found in: C:\Videos
```

### Solutions

#### Check 1: Verify file extensions
Supported formats: `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv`, `.wmv`

#### Check 2: Check folder path
```powershell
# Use quotes for paths with spaces
python main_app.py --batch-folder "C:\My Videos"
```

#### Check 3: Verify files exist
```powershell
dir "C:\Videos\*.mp4"
```

---

## ❌ Build .exe Fails

### Problem
PyInstaller build fails or .exe doesn't work.

### Solutions

#### Check 1: Verify PyInstaller is installed
```powershell
pip show pyinstaller
```

If not:
```powershell
pip install pyinstaller
```

#### Check 2: Clean previous builds
```powershell
# Delete old builds
Remove-Item -Recurse -Force build, dist
Remove-Item *.spec

# Rebuild
.\build_exe.ps1
```

#### Check 3: Check for missing dependencies
```powershell
# Reinstall all requirements
pip install -r requirements_gui_pinned.txt
```

---

## ❌ .exe is Too Large

### Problem
Built .exe is over 2 GB.

### Solutions

#### Option 1: Don't bundle Whisper models
```powershell
# When prompted, choose "No" for bundling models
.\build_exe_bundled.ps1
```

#### Option 2: Use CPU-only build
```powershell
# Uninstall CUDA PyTorch
pip uninstall torch torchvision torchaudio -y

# Install CPU-only version
pip install -r requirements_gui_cpu.txt

# Build (will be ~200 MB smaller)
.\build_exe.ps1
```

#### Option 3: Use basic build
```powershell
# Don't bundle FFmpeg
.\build_exe.ps1
```

---

## ❌ Antivirus Flags .exe

### Problem
Windows Defender or antivirus flags the .exe as malware.

### Solutions

#### Option 1: Add exception
- Open Windows Security
- Virus & threat protection
- Manage settings
- Add exclusion
- Add your .exe file

#### Option 2: Code sign (advanced)
- Requires code signing certificate
- See: https://pyinstaller.org/en/stable/usage.html#windows-code-signing

#### Option 3: Provide source code
- Share the source code alongside .exe
- Users can verify and build themselves

---

## ❌ Slow Processing Speed

### Problem
Video processing is very slow.

### Solutions

#### Check 1: Use GPU mode
```powershell
# Make sure using CUDA
python main_app.py --input "video.mp4" --device cuda
```

#### Check 2: Use faster preset
```powershell
# Use preset 10-13 for faster encoding (lower quality)
python main_app.py --input "video.mp4" --preset 13
```

#### Check 3: Lower resolution
```powershell
# Encode to 720p instead of 1080p
python main_app.py --input "video.mp4" --resolution 720
```

#### Check 4: Check GPU usage
- Open Task Manager → Performance → GPU
- Should show high usage during subtitle generation

---

## ❌ Subtitles Not Generated

### Problem
Video encodes but no subtitles are created.

### Solutions

#### Check 1: Verify Whisper is installed
```powershell
pip show whisper-ctranslate2
```

#### Check 2: Check for errors in output
Look for error messages during Stage 2 (AI Subtitles)

#### Check 3: Test Whisper separately
```powershell
whisper-ctranslate2 "test_video.mp4" --model small --task translate --language ja
```

#### Check 4: Check audio track
- Video must have audio
- Audio should be Japanese (or change `--language ja`)

---

## ❌ Virtual Environment Issues

### Problem
Packages installed but not found.

### Solutions

#### Check if in virtual environment
```powershell
# Check current Python
python -c "import sys; print(sys.executable)"
```

#### Activate virtual environment
```powershell
# If using venv
.\venv\Scripts\activate

# Then install requirements
pip install -r requirements_gui_pinned.txt
```

#### Or use global Python
```powershell
# Deactivate venv
deactivate

# Install globally
pip install -r requirements_gui_pinned.txt
```

---

## 🔍 Diagnostic Commands

### Check Python Version
```powershell
python --version
```

### Check Installed Packages
```powershell
pip list
```

### Check Specific Package
```powershell
pip show gooey
pip show whisper-ctranslate2
pip show torch
```

### Check CUDA Availability
```powershell
python -c "import torch; print('CUDA Available:', torch.cuda.is_available())"
```

### Check FFmpeg
```powershell
ffmpeg -version
```

### Run Installation Test
```powershell
python test_installation.ps1
```

---

## 📞 Still Having Issues?

### Step 1: Run Diagnostic
```powershell
python test_installation.ps1
```

### Step 2: Reinstall Requirements
```powershell
pip uninstall -r requirements_gui.txt -y
pip install -r requirements_gui_pinned.txt
```

### Step 3: Force Reinstall Critical Packages
```powershell
pip install --force-reinstall --no-cache-dir six colored==1.4.4 gooey
```

### Step 4: Check Documentation
- [INSTALLATION_SUCCESS.md](INSTALLATION_SUCCESS.md) - Installation guide
- [QUICKSTART_GUI.md](QUICKSTART_GUI.md) - Quick start
- [GUI_README.md](GUI_README.md) - Full documentation

---

## 📝 Reporting Issues

If you're still stuck, gather this information:

```powershell
# Python version
python --version

# Installed packages
pip list > installed_packages.txt

# CUDA check
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

# Error message (copy full traceback)
python main_app.py > error.txt 2>&1
```

---

**Last Updated**: 2026-02-05
