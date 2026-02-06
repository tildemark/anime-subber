# 🚀 Quick Start - AnimeSubber GUI

## First Time Setup (Run Once)

```powershell
# Install all dependencies
.\setup.ps1
```

This installs everything you need including the problematic `six` and `colored` packages.

---

## Launch the Application

```powershell
# GUI Mode (recommended)
python main_app.py

# CLI Mode
python main_app.py --help
```

---

## If You Get "ModuleNotFoundError: No module named 'six'"

This happens in new terminal sessions. Quick fix:

```powershell
pip install --force-reinstall --no-cache-dir six colored==1.4.4
```

Or just run the setup script again:

```powershell
.\setup.ps1
```

---

## Build Standalone .exe

```powershell
.\build_exe.ps1
```

The .exe will be in: `dist\AnimeSubber.exe`

---

## Files You Need

- **setup.ps1** - Install dependencies (run once)
- **main_app.py** - The application
- **build_exe.ps1** - Build .exe file

---

## Complete Documentation

- [docs/INSTALLATION_SUCCESS.md](docs/INSTALLATION_SUCCESS.md) - Full installation guide
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Fix common issues
- [docs/GUI_README.md](docs/GUI_README.md) - Complete documentation

---

**Last Updated**: 2026-02-06
