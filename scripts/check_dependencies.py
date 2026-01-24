"""
===================================
DEPENDENCY CHECKER
===================================
check_dependencies.py

Verifies that all required dependencies are installed and properly configured.
Checks for FFmpeg, Python packages, and CUDA support.

USAGE:
  python scripts/check_dependencies.py

USAGE (Wrapper Scripts):
  Windows PowerShell: .\wrappers\ps1\check_dependencies.ps1
  Linux/macOS:       ./wrappers/sh/check_dependencies.sh
"""

import sys
import subprocess
import importlib.util
import os

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    print("🔍 Checking FFmpeg...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Extract version info
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ FFmpeg is installed: {version_line}")
            return True
        else:
            print("  ❌ FFmpeg found but returned an error")
            return False
    except FileNotFoundError:
        print("  ❌ FFmpeg not found in PATH")
        print("     Install from: https://www.gyan.dev/ffmpeg/builds/ (Windows)")
        print("     Or run: sudo apt install ffmpeg (Linux)")
        print("     Or run: brew install ffmpeg (macOS)")
        return False
    except Exception as e:
        print(f"  ❌ Error checking FFmpeg: {e}")
        return False

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown version')
            print(f"  ✅ {package_name} is installed ({version})")
            return True
        except Exception as e:
            print(f"  ⚠️  {package_name} found but cannot import: {e}")
            return False
    else:
        print(f"  ❌ {package_name} is not installed")
        return False

def check_cuda():
    """Check if CUDA is available for PyTorch"""
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
            print(f"  ✅ CUDA is available: {device_name}")
            print(f"     Devices: {device_count}, Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            return True
        else:
            print("  ⚠️  PyTorch is installed but CUDA is not available")
            print("     You may need to reinstall PyTorch with CUDA support:")
            print("     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
            return False
    except ImportError:
        print("  ❌ PyTorch (torch) is not installed")
        return False

def main():
    """Main dependency check routine"""
    print("=" * 60)
    print("🔧 ANIME SUBBER - DEPENDENCY CHECK")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check FFmpeg
    if not check_ffmpeg():
        all_ok = False
    print()
    
    # Check Python version
    print("🔍 Checking Python version...")
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 8:
        print(f"  ✅ Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        print(f"  ❌ Python {py_version.major}.{py_version.minor}.{py_version.micro} (requires 3.8+)")
        all_ok = False
    print()
    
    # Check required Python packages
    print("🔍 Checking Python packages...")
    packages = {
        'whisper-ctranslate2': 'faster_whisper',
        'torch': 'torch',
    }
    
    for pkg_name, import_name in packages.items():
        if not check_python_package(pkg_name, import_name):
            all_ok = False
    print()
    
    # Check CUDA
    print("🔍 Checking CUDA support...")
    if not check_cuda():
        print("     ⚠️  Warning: Without CUDA, subtitle generation will be very slow")
    print()
    
    # Final summary
    print("=" * 60)
    if all_ok:
        print("✅ ALL DEPENDENCIES OK - Ready to use!")
    else:
        print("❌ SOME DEPENDENCIES MISSING - Please install them first")
        print("\nQuick Install:")
        print("  pip install whisper-ctranslate2")
        print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
