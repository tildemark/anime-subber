### **README.md**

# Anime AV1 Subber 🎥 🤖

An automated Python pipeline to convert high-resolution Japanese anime into efficient **AV1** format and generate **AI-translated English subtitles** locally.

This project is specifically optimized for mid-range hardware (tested on **Ryzen 2600** and **NVIDIA GTX 1050 2GB VRAM**) to handle long-form movies without system lag or memory crashes.

## 🌟 Features
- **Modern Compression:** Uses `SVT-AV1` for superior quality-to-size ratio.
- **AI Translation:** Leverages `Whisper-CTranslate2` to turn Japanese audio into English `.srt` files.
- **VAD Integration:** Voice Activity Detection skips silent/action scenes to prevent AI hallucinations.
- **Resource Friendly:** Runs with low-priority flags to keep your OS responsive.
- **Automated Muxing:** Automatically packages video and subtitles into a single `.mkv` container.

## 🛠️ Prerequisites

### 1. FFmpeg
Required for video encoding and muxing.
- Download from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
- Add `bin/ffmpeg.exe` to your System **PATH**.

### 2. Python Dependencies
Ensure you have Python 3.8+ installed. It is highly recommended to use a GPU with CUDA support.

```bash
# Install the optimized Whisper engine
pip install whisper-ctranslate2

# Install Torch with CUDA support (for NVIDIA GPUs)
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)

```

## 🚀 Usage

Run the script from your terminal:

```bash
python auto_anime.py <input_file> <output_name.mkv> [resolution]

```

### Examples:

**Convert and subtitle at original resolution:**

```bash
python auto_anime.py movie.mp4 output.mkv

```

**Downscale to 1440p and subtitle:**

```bash
python auto_anime.py raw_4k_source.mp4 movie_1440p.mkv 1440

```

## 🏗️ How it Works

The pipeline runs in three distinct stages:

1. **Stage 1 (CPU):** Encodes video to AV1 and audio to Opus. Using a low-priority flag allows the Ryzen 2600 to handle the heavy encoding without freezing your PC.
2. **Stage 2 (GPU):** Runs the `small` Whisper model with `int8` quantization. This fits the model entirely within **2GB of VRAM**, ensuring speed and stability.
3. **Stage 3 (Mux):** Uses FFmpeg to "remux" the new video and the AI-generated `.srt` into a final `.mkv` with proper metadata.

## ⚙️ Configuration for Low VRAM

If you have exactly 2GB of VRAM, the script is pre-configured with:

* `--model small`: The best accuracy-to-memory ratio.
* `--compute_type int8`: Reduces memory footprint significantly.
* `--vad_filter True`: Skips non-speech segments to save processing time.

## 📄 License

MIT

---

Maintainer: [tildemark](https://www.google.com/search?q=https://github.com/tildemark) | Website: [sanchez.ph](https://sanchez.ph)

```
