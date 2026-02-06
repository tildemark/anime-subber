# Changelog

All notable changes to the Anime Subber project are documented here.

## [2.0.0] - February 6, 2026

### Added - GUI Application 🎉
- **Windows Desktop Application**: Complete GUI built with Gooey framework
  - `main_app.py` - Hybrid GUI/CLI application with automatic mode detection
  - Standard readable theme for better usability
  - Mutually exclusive input group (single file OR batch folder)
  - Hardware configuration dropdowns (CUDA/CPU, resolution, SVT-AV1 preset)
  - Optional PC shutdown after batch completion
  - PyInstaller bundling support with FFmpeg detection

- **Build & Distribution Tools**:
  - `build_exe.ps1` - Basic PyInstaller build script (~500 MB .exe)
  - `build_exe_bundled.ps1` - Bundled build with FFmpeg included
  - `download_ffmpeg.ps1` - Automated FFmpeg download for bundling
  - `download_whisper_models.ps1` - Whisper model download for offline use
  - `setup.ps1` - One-command dependency installation

- **Requirements Files**:
  - `requirements_gui.txt` - Flexible versions with CUDA support
  - `requirements_gui_pinned.txt` - Stable pinned versions (recommended)
  - `requirements_gui_cpu.txt` - CPU-only version for systems without GPU

- **Comprehensive Documentation** (12 new guides):
  - `QUICKSTART.md` - 2-minute quick start guide
  - `docs/GUI_README.md` - Complete GUI documentation
  - `docs/QUICKSTART_GUI.md` - 5-minute GUI quick start
  - `docs/REQUIREMENTS_GUIDE.md` - Requirements file comparison
  - `docs/BUNDLING_GUIDE.md` - Complete bundling & distribution guide
  - `docs/TROUBLESHOOTING.md` - Comprehensive troubleshooting
  - `docs/INSTALLATION_SUCCESS.md` - Installation verification
  - `docs/SETUP_COMPLETE.md` - Setup summary
  - `docs/PROJECT_STRUCTURE.md` - Project organization
  - `docs/PACKAGE_SUMMARY.md` - Package overview
  - `docs/GUI_ARCHITECTURE.md` - Technical architecture diagrams
  - `docs/README.md` - Documentation index

- **Testing & Examples**:
  - `test_installation.ps1` - Automated dependency verification
  - `examples_cli.ps1` - CLI usage examples and automation templates

### Changed
- **Documentation Organization**: 
  - Moved all documentation except README.md and CHANGELOG.md to `docs/` folder
  - Created comprehensive documentation index in `docs/README.md`
  - Updated all cross-references in README.md and QUICKSTART.md

- **README.md**: 
  - Added GUI application section with features and quick start
  - Updated installation instructions to use `setup.ps1`
  - Simplified quick start to 2 commands

- **UI Theme**: Changed from dark theme to standard Gooey theme for better readability

### Fixed
- **Dependency Issues**:
  - Added `six` package to all requirements files (required by Gooey)
  - Pinned `colored==1.4.4` for Gooey compatibility (v2.x breaks Gooey)
  - Fixed widget parameter handling for CLI mode compatibility

- **Build Script**: Simplified `build_exe.ps1` to avoid PowerShell syntax issues

### Technical Details
- **Bundled FFmpeg Support**: Application automatically detects bundled FFmpeg in PyInstaller executables via `sys._MEIPASS`
- **VAD Filter Escaping**: Proper JSON escaping for Whisper VAD parameters on Windows
- **Low Priority Processing**: Uses `creationflags=0x00004000` for Windows background processing
- **Hybrid Architecture**: Single codebase supports both GUI (Gooey) and CLI (argparse) modes

### Repository Structure
- Added `.gitignore` to exclude build artifacts, bundled resources, and temporary files
- Clean root directory with only essential files
- All documentation organized in `docs/` folder

---

## [1.2.1] - February 5, 2026

### Added
- **Local FFmpeg auto-detection**: `encode_simple.py` and `encode_smart.py` now use a bundled `ffmpeg.exe` if present (Windows), otherwise fall back to PATH.
- **GPU encoding option in `encode_smart.py`**: Optional HEVC NVENC path for faster encodes on NVIDIA GPUs.
- **Batch benchmarking in `encode_smart.py`**: Benchmarks the first file and applies the selected option to the batch.
- **More encoding options**: Added options 5 and 6 in the interactive menu for smaller file variants.

### Changed
- **Batch flow in `encode_smart.py`**: Now interactive with benchmarking and selectable presets instead of fixed defaults.
- **PowerShell wrapper guidance**: `encode_smart.ps1` usage text and feature list now reflect GPU choice and expanded options.

### Fixed
- **Benchmark stability**: Avoids divide-by-zero when timing is extremely short and reports ffmpeg errors cleanly.

## [1.2.0] - January 24, 2026

### Added
- **Dependency Checker Tool**: 
  - New `check_dependencies.py` script verifies all requirements
  - Checks FFmpeg installation and PATH configuration
  - Verifies Python version (3.8+) and required packages
  - Tests CUDA availability for GPU acceleration
  - Wrapper scripts: `check_dependencies.ps1` (Windows) and `check_dependencies.sh` (Linux/macOS)

- **Organized Folder Structure**: 
  - `scripts/` - All 8 Python executables in one place
  - `wrappers/ps1/` - PowerShell wrapper scripts for Windows
  - `wrappers/sh/` - Shell wrapper scripts for Linux/macOS
  - `docs/` - Additional documentation (flowcharts, diagrams)
  - README.md and CHANGELOG.md remain in root for GitHub visibility

- **Wrapper Scripts for Easy Execution**:
  - Linux/macOS: 8 shell scripts (`.sh`) for all Python scripts
  - Windows: 8 PowerShell scripts (`.ps1`) for all Python scripts
  - Wrapper scripts handle Python path detection and error checking
  - Users can now run: `.\wrappers\ps1\pipeline_windows.ps1 movie.mp4` instead of `python scripts/pipeline_windows.py movie.mp4`

- **Improved Documentation in Docstrings**: All Python scripts now show usage examples for both direct Python and wrapper scripts

- **File Renaming for Clarity**: More meaningful script names:
  - `convert.py` → `encode_simple.py`
  - `convert2.py` → `encode_smart.py`
  - `translate_only.py` → `add_subtitles.py`
  - `auto_anime_win.py` → `pipeline_windows.py`
  - `auto_anime_unix.py` → `pipeline_unix.py`
  - `bench.py` → `benchmark.py`
  - `benchmark_convert.py` → `bench_encoding.py`

### Changed
- **README.md**: 
  - Updated with project structure diagram and clear explanation of organizational benefits
  - Added detailed FFmpeg installation instructions for Windows/Linux/macOS
  - Added step-by-step guide for setting Windows PATH environment variable (GUI and PowerShell methods)
  - Included dependency verification section with wrapper script examples
  - Added comprehensive "Running Scripts From Any Folder" section with practical examples
  - Updated Quick Start to show both project directory and external directory usage
  - Enhanced "Next Steps" with numbered setup instructions
- **Script Docstrings**: Now include both direct Python and wrapper script usage examples
- **User Interface**: All wrapper scripts provide color-coded output and helpful error messages
- **Path Resolution**: All wrappers intelligently locate scripts using relative path calculations

### Shell Scripts (Linux/macOS)
- `encode_simple.sh` - Simple video encoding wrapper
- `encode_smart.sh` - Smart encoding with benchmarking wrapper
- `add_subtitles.sh` - Subtitle generation wrapper
- `pipeline_windows.sh` - Windows pipeline wrapper (for reference)
- `pipeline_unix.sh` - Unix/Linux pipeline wrapper
- `benchmark.sh` - Hardware benchmarking wrapper
- `bench_encoding.sh` - Encoding benchmark wrapper

### PowerShell Scripts (Windows)
- `encode_simple.ps1` - Simple video encoding wrapper
- `encode_smart.ps1` - Smart encoding with benchmarking wrapper
- `add_subtitles.ps1` - Subtitle generation wrapper
- `pipeline_windows.ps1` - Windows pipeline wrapper
- `pipeline_unix.ps1` - Unix/Linux pipeline wrapper (for WSL)
- `benchmark.ps1` - Hardware benchmarking wrapper
- `bench_encoding.ps1` - Encoding benchmark wrapper

---

## [1.1.0] - January 24, 2026

### Added
- **Batch Processing Support**: All scripts now support wildcard patterns (e.g., `*.mp4`, `videos/*.mkv`)
- **Comprehensive Comments**: All Python files now include detailed docstrings and inline comments
- **Auto-Shutdown Option**: Windows version supports auto-shutdown after encoding completes
- **Benchmark Script**: Quick hardware testing tool to estimate encoding times
- **Subtitle-Only Mode**: Dedicated script for adding subtitles to already-encoded videos
- **Smart Encoding**: encode_smart.py provides interactive preset selection with time/size estimates
- **Consolidated Documentation**: All guides merged into README.md for easier navigation

### Changed
- **README.md**: Now includes complete documentation (Quick Start, Script Comparison, Configuration, Troubleshooting)
- **Documentation Structure**: Reduced from 7+ markdown files to just README.md + VISUAL_OVERVIEW.md + CHANGELOG.md
- **Script Output**: Enhanced with better status messages, progress indicators, and visual formatting
- **User Interface**: All scripts now show clear progress ([1/3], [2/3], [3/3] stages) with emoji indicators

### Removed
- **encode_simple_v1.py**: Deleted backup file (was identical to encode_simple.py)
- **Multiple Documentation Files**: Consolidated into single README.md

### Fixed
- Improved error messages and troubleshooting guidance
- Better path handling for cross-platform compatibility
- Clearer parameter documentation in all scripts

---

## [1.0.0] - Initial Release

### Features
- SVT-AV1 video encoding with Opus audio
- Whisper-CTranslate2 AI subtitle generation
- Full pipeline automation (encode → translate → mux)
- Low-priority execution for system responsiveness
- Support for Windows, Linux, and macOS
- VAD (Voice Activity Detection) for subtitle accuracy
- Customizable resolution, preset, and CRF settings
- Batch processing support

### Scripts Included
- `auto_anime_win.py` - Complete pipeline for Windows
- `auto_anime_unix.py` - Complete pipeline for Linux/macOS
- `convert.py` - Basic video encoding
- `convert2.py` - Smart encoding with benchmarking
- `bench.py` - Hardware benchmarking tool
- `translate_only.py` - Subtitle generation only
