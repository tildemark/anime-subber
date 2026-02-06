# Requirements Files Guide

This project provides **4 different requirements files** to suit different needs:

---

## 📋 Available Requirements Files

### 1️⃣ **requirements_gui.txt** (Recommended for most users)

**What it does**: Installs the latest compatible versions with CUDA support

**Use when**:
- ✅ You have an NVIDIA GPU
- ✅ You want the latest features
- ✅ You're okay with potential compatibility issues

**Install**:
```powershell
pip install -r requirements_gui.txt
```

**Pros**:
- Latest features and bug fixes
- Automatic updates to compatible versions
- CUDA GPU acceleration

**Cons**:
- May have compatibility issues with new releases
- Larger download (~3-4 GB with CUDA)

---

### 2️⃣ **requirements_gui_pinned.txt** (Recommended for production)

**What it does**: Installs specific tested versions with CUDA support

**Use when**:
- ✅ You need stability and reproducibility
- ✅ You're deploying to production
- ✅ You want to avoid breaking changes
- ✅ You have an NVIDIA GPU

**Install**:
```powershell
pip install -r requirements_gui_pinned.txt
```

**Pros**:
- Guaranteed compatibility
- Reproducible builds
- Tested and stable
- CUDA GPU acceleration

**Cons**:
- May miss latest features
- Requires manual updates
- Larger download (~3-4 GB with CUDA)

**Versions included** (as of 2026-02-05):
- gooey==1.0.8.1
- whisper-ctranslate2==0.4.3
- torch==2.2.0 (CUDA 12.1)
- pyinstaller==6.3.0

---

### 3️⃣ **requirements_gui_cpu.txt** (For systems without GPU)

**What it does**: Installs latest versions with CPU-only PyTorch

**Use when**:
- ✅ You don't have an NVIDIA GPU
- ✅ You want smaller installation size
- ✅ You only need CPU processing
- ✅ You're testing or developing

**Install**:
```powershell
pip install -r requirements_gui_cpu.txt
```

**Pros**:
- Much smaller download (~500 MB)
- Works on any PC
- No CUDA drivers needed
- Faster installation

**Cons**:
- Slower AI subtitle generation (5-10x slower)
- No GPU acceleration

---

### 4️⃣ **requirements.txt** (Original CLI version)

**What it does**: Minimal dependencies for CLI scripts only (if it exists)

**Use when**:
- ✅ You only want to use CLI scripts
- ✅ You don't need the GUI
- ✅ You want minimal installation

---

## 🎯 Quick Decision Guide

### "I have an NVIDIA GPU and want it to just work"
→ Use **requirements_gui.txt**

### "I need stability for a production deployment"
→ Use **requirements_gui_pinned.txt**

### "I don't have an NVIDIA GPU"
→ Use **requirements_gui_cpu.txt**

### "I only want CLI scripts, no GUI"
→ Use **requirements.txt** (if available) or install manually

---

## 📊 Comparison Table

| Feature | requirements_gui.txt | requirements_gui_pinned.txt | requirements_gui_cpu.txt |
|---------|---------------------|----------------------------|-------------------------|
| **GPU Support** | ✅ CUDA | ✅ CUDA | ❌ CPU only |
| **Version Pinning** | ❌ Latest | ✅ Pinned | ❌ Latest |
| **Download Size** | ~3-4 GB | ~3-4 GB | ~500 MB |
| **Stability** | ⚠️ May vary | ✅ Guaranteed | ⚠️ May vary |
| **AI Speed** | ⚡⚡⚡ Fast | ⚡⚡⚡ Fast | 🐌 Slow |
| **Best For** | Development | Production | No GPU |

---

## 🔄 Switching Between Versions

### From GPU to CPU-only

```powershell
# Uninstall GPU versions
pip uninstall torch torchvision torchaudio -y

# Install CPU versions
pip install -r requirements_gui_cpu.txt
```

### From CPU to GPU

```powershell
# Uninstall CPU versions
pip uninstall torch torchvision torchaudio -y

# Install GPU versions
pip install -r requirements_gui.txt
```

### From Flexible to Pinned

```powershell
# Uninstall all
pip uninstall -r requirements_gui.txt -y

# Install pinned versions
pip install -r requirements_gui_pinned.txt
```

---

## 🛠️ Installation Examples

### Fresh Installation (GPU, Latest)

```powershell
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements_gui.txt

# Verify installation
python test_installation.ps1
```

### Fresh Installation (GPU, Pinned)

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install pinned dependencies
pip install -r requirements_gui_pinned.txt

# Verify installation
python test_installation.ps1
```

### Fresh Installation (CPU-only)

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install CPU dependencies
pip install -r requirements_gui_cpu.txt

# Verify installation
python test_installation.ps1
```

---

## 📦 Building .exe with Different Versions

All requirements files work with PyInstaller:

```powershell
# Works with any requirements file
.\build_exe.ps1
```

**Note**: The .exe will include the PyTorch version you installed:
- GPU version: ~500 MB executable
- CPU version: ~200 MB executable

---

## 🔍 Checking What's Installed

```powershell
# List all installed packages
pip list

# Check specific package versions
pip show gooey
pip show torch
pip show whisper-ctranslate2

# Check if CUDA is available
python -c "import torch; print('CUDA' if torch.cuda.is_available() else 'CPU')"
```

---

## ⚠️ Common Issues

### "No module named 'torch'"

**Solution**: Install PyTorch
```powershell
pip install -r requirements_gui.txt
```

### "CUDA out of memory"

**Solution**: Switch to CPU mode or close other GPU applications
```powershell
# Option 1: Use CPU in the app
python main_app.py --device cpu

# Option 2: Switch to CPU-only PyTorch
pip uninstall torch torchvision torchaudio -y
pip install -r requirements_gui_cpu.txt
```

### "Package conflicts"

**Solution**: Use pinned versions
```powershell
pip uninstall -r requirements_gui.txt -y
pip install -r requirements_gui_pinned.txt
```

---

## 📝 Creating Your Own Requirements File

You can create a custom requirements file:

```powershell
# Export current environment
pip freeze > requirements_custom.txt

# Edit to keep only needed packages
notepad requirements_custom.txt

# Install from custom file
pip install -r requirements_custom.txt
```

---

## 🎓 Best Practices

1. **Use virtual environments**: Isolate project dependencies
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Pin versions for production**: Use `requirements_gui_pinned.txt`

3. **Test before deploying**: Use `test_installation.ps1`

4. **Document your choice**: Note which requirements file you used

5. **Update regularly**: Check for security updates
   ```powershell
   pip list --outdated
   ```

---

## 📞 Need Help?

- **Installation issues**: Run `python test_installation.ps1`
- **GPU not detected**: Check NVIDIA drivers and CUDA installation
- **Package conflicts**: Try pinned versions
- **Slow performance**: Verify GPU is being used

---

**Last Updated**: 2026-02-05
