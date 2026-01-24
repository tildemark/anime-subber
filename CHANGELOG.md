# Changelog

All notable changes to the Anime Subber project are documented here.

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
