# 🎉 Version 2.0.0 - GUI Application Release

## What's New

**AnimeSubber now has a complete Windows Desktop Application!**

### ✨ Major Features

#### 🖥️ GUI Application
- **Hybrid GUI/CLI**: Automatic mode detection - GUI when no arguments, CLI when arguments provided
- **User-Friendly Interface**: Standard readable theme with file/folder choosers
- **Batch Processing**: Process entire folders of videos automatically
- **Hardware Configuration**: Easy dropdowns for CUDA/CPU, resolution, and encoding presets
- **Auto-Shutdown**: Optional PC shutdown after batch completion
- **Standalone .exe**: Build once, share with anyone (no Python installation required)

#### 📦 Build & Distribution
- **Basic Build**: `build_exe.ps1` - Creates ~500 MB executable
- **Bundled Build**: `build_exe_bundled.ps1` - Includes FFmpeg for complete standalone distribution
- **FFmpeg Bundling**: Automated download and packaging with `download_ffmpeg.ps1`
- **Whisper Models**: Optional offline model bundling with `download_whisper_models.ps1`

#### 📚 Documentation
- **12 New Guides**: Comprehensive documentation covering installation, usage, troubleshooting, and building
- **Organized Structure**: All docs moved to `docs/` folder with index
- **Quick Start**: Get running in 2 minutes with `QUICKSTART.md`

---

## 🚀 Quick Start

### Install Dependencies
```powershell
.\setup.ps1
```

### Launch GUI
```powershell
python main_app.py
```

### Build Standalone .exe
```powershell
.\build_exe.ps1
```

---

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 2 minutes
- **[docs/GUI_README.md](docs/GUI_README.md)** - Complete GUI documentation
- **[docs/BUNDLING_GUIDE.md](docs/BUNDLING_GUIDE.md)** - Build & distribution guide
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Fix common issues
- **[docs/README.md](docs/README.md)** - Complete documentation index

---

## 🔧 What Changed

### Repository Structure
- ✅ Clean root directory (only README.md, CHANGELOG.md, QUICKSTART.md)
- ✅ All documentation in `docs/` folder
- ✅ Added `.gitignore` for build artifacts

### Dependencies
- ✅ Added `six` package (required by Gooey)
- ✅ Pinned `colored==1.4.4` (Gooey compatibility)
- ✅ Three requirements files: flexible, pinned, and CPU-only

### UI/UX
- ✅ Standard readable theme (removed dark mode)
- ✅ Improved error messages
- ✅ One-command setup with `setup.ps1`

---

## 📊 Files Added

### Core Application
- `main_app.py` - Hybrid GUI/CLI application

### Build Scripts
- `build_exe.ps1` - Basic build
- `build_exe_bundled.ps1` - Bundled build
- `download_ffmpeg.ps1` - FFmpeg download
- `download_whisper_models.ps1` - Model download
- `setup.ps1` - Dependency installation

### Requirements
- `requirements_gui.txt` - Flexible versions
- `requirements_gui_pinned.txt` - Stable versions
- `requirements_gui_cpu.txt` - CPU-only

### Documentation (in docs/)
- 12 comprehensive guides
- Documentation index

### Testing & Examples
- `test_installation.ps1` - Dependency verification
- `examples_cli.ps1` - CLI usage examples

---

## 🎯 Upgrade Path

### From v1.x CLI Scripts

The original CLI scripts are still fully functional! The GUI is an addition, not a replacement.

**To use the new GUI:**
1. Run `.\setup.ps1` to install GUI dependencies
2. Launch with `python main_app.py`

**To keep using CLI:**
- All original scripts in `scripts/` folder still work
- No changes required

---

## 💡 Benefits

### For Desktop Users
- ✅ No command line needed
- ✅ Visual file/folder selection
- ✅ Easy configuration with dropdowns
- ✅ Progress tracking in GUI

### For Power Users
- ✅ Full CLI support maintained
- ✅ Automation-friendly
- ✅ Scriptable with examples provided

### For Distribution
- ✅ Build standalone .exe
- ✅ Optional FFmpeg bundling
- ✅ No Python installation required for end users

---

## 🔗 Links

- **Main README**: [README.md](README.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Documentation**: [docs/README.md](docs/README.md)

---

**Released**: February 6, 2026  
**Version**: 2.0.0  
**Type**: Major Release - GUI Application
