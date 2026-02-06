# GUI Application Architecture

## Overview

The `main_app.py` provides a **hybrid GUI/CLI interface** for the anime-subber pipeline, built using the Gooey library.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERACTION                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐              ┌──────────────────┐     │
│  │   GUI Mode       │              │   CLI Mode       │     │
│  │  (No arguments)  │              │  (With args)     │     │
│  │                  │              │                  │     │
│  │  • File chooser  │              │  --input file    │     │
│  │  • Folder picker │              │  --batch-folder  │     │
│  │  • Dropdowns     │              │  --device cuda   │     │
│  │  • Checkboxes    │              │  --resolution    │     │
│  │                  │              │  --preset        │     │
│  └────────┬─────────┘              └────────┬─────────┘     │
│           │                                 │               │
│           └─────────────┬───────────────────┘               │
│                         │                                   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   MAIN_APP.PY CORE                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Argument Parser (GooeyParser / ArgumentParser)    │     │
│  │  • Mutually exclusive input group                  │     │
│  │  • Hardware & performance options                  │     │
│  │  • Post-task action settings                       │     │
│  └────────────────────┬───────────────────────────────┘     │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Input Validation & File Discovery                 │     │
│  │  • Single file: Validate path exists              │     │
│  │  • Batch folder: Auto-detect video files          │     │
│  │  • Supported: .mp4, .mkv, .avi, .mov              │     │
│  └────────────────────┬───────────────────────────────┘     │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Processing Pipeline Dispatcher                    │     │
│  │  • Single file → process_single_file()            │     │
│  │  • Multiple files → process_batch()               │     │
│  └────────────────────┬───────────────────────────────┘     │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  PROCESSING PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  STAGE 1: VIDEO ENCODING (encode_video)             │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │  • Input: Original video file                  │ │   │
│  │  │  • Codec: SVT-AV1 (libsvtav1)                  │ │   │
│  │  │  • Audio: Opus @ 128kbps                       │ │   │
│  │  │  • Scaling: Based on resolution setting        │ │   │
│  │  │  • Priority: Low (0x00004000)                  │ │   │
│  │  │  • Output: {filename}_encoded.mkv              │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  STAGE 2: AI SUBTITLE GENERATION (generate_subtitles)│  │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │  • Input: Original video file                  │ │   │
│  │  │  • Engine: whisper-ctranslate2                 │ │   │
│  │  │  • Model: small (int8 quantization)            │ │   │
│  │  │  • Task: Translate (Japanese → English)        │ │   │
│  │  │  • Device: CUDA or CPU (user choice)           │ │   │
│  │  │  • VAD Filter: JSON-escaped parameters         │ │   │
│  │  │  • Output: {filename}.srt                      │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  STAGE 3: MUXING (mux_subtitles)                     │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │  • Input: Encoded video + SRT file             │ │   │
│  │  │  • Tool: FFmpeg (stream copy)                  │ │   │
│  │  │  • Metadata: Language tags, title              │ │   │
│  │  │  • Output: {filename}_final.mkv                │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   POST-PROCESSING                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Batch Processing (if multiple files)              │     │
│  │  • Process files sequentially                      │     │
│  │  • Track completed and failed files                │     │
│  │  • Display summary report                          │     │
│  └────────────────────┬───────────────────────────────┘     │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Shutdown Management (if enabled)                  │     │
│  │  • Only triggers after ALL files complete          │     │
│  │  • 60-second delay (cancellable)                   │     │
│  │  • Command: shutdown /s /t 60                      │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Gooey Decorator

```python
@Gooey(
    program_name="Anime Subber",
    navigation='SIDEBAR',
    header_bg_color='#1a1a2e',
    # ... styling options
)
```

**Purpose**: Automatically generates GUI from argparse configuration

**Behavior**:
- GUI mode: `len(sys.argv) == 1` (no arguments)
- CLI mode: `len(sys.argv) > 1` (arguments provided)

### 2. Argument Parser

**Mutually Exclusive Group**:
```python
input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument('--input', widget='FileChooser')
input_group.add_argument('--batch-folder', widget='DirChooser')
```

**Hardware Options**:
- `--device`: CUDA or CPU
- `--resolution`: source, 1440, 1080, 720
- `--preset`: 0-13 (SVT-AV1 speed/quality)

**Post-Task Action**:
- `--shutdown`: Checkbox/flag for PC shutdown

### 3. Processing Functions

#### `encode_video()`
- Uses FFmpeg with SVT-AV1 codec
- Applies resolution scaling
- Runs at low priority (Windows flag: 0x00004000)
- Anime-optimized parameters

#### `generate_subtitles()`
- Uses whisper-ctranslate2
- Properly escapes VAD filter JSON for Windows
- Supports CUDA and CPU modes
- Translates Japanese → English

#### `mux_subtitles()`
- Combines video + SRT using FFmpeg
- Stream copy (no re-encoding)
- Adds language metadata

### 4. Batch Processing

```python
def process_batch(files, device, resolution, preset, shutdown_after):
    for file in files:
        process_single_file(file, ...)
    
    if shutdown_after:
        os.system("shutdown /s /t 60")
```

**Features**:
- Sequential processing (one at a time)
- Error tracking
- Summary report
- Shutdown only after ALL files

---

## Data Flow

```
User Input
    │
    ├─ GUI Mode: File/Folder chooser, dropdowns
    │             ↓
    │         GooeyParser
    │
    └─ CLI Mode: Command-line arguments
                  ↓
              ArgumentParser
    
    ↓
    
Validation & Discovery
    │
    ├─ Single file: Check exists
    └─ Batch folder: Glob for videos
    
    ↓
    
Processing Pipeline (per file)
    │
    ├─ Stage 1: Video → AV1 (40-80 hours)
    ├─ Stage 2: Audio → SRT (~30 minutes)
    └─ Stage 3: Mux → Final MKV (~1 minute)
    
    ↓
    
Post-Processing
    │
    ├─ Batch: Summary report
    └─ Shutdown: Optional PC shutdown
```

---

## Key Technical Details

### Windows Low Priority

```python
LOW_PRIORITY = 0x00004000  # BELOW_NORMAL_PRIORITY_CLASS
subprocess.run(cmd, creationflags=LOW_PRIORITY)
```

**Effect**: Keeps system responsive during long encodes

### VAD Filter Escaping

```python
# ❌ WRONG (Windows error)
"--vad_parameters", "{'min_silence_duration_ms': 500}"

# ✅ CORRECT
vad_params = json.dumps({"min_silence_duration_ms": 500})
"--vad_parameters", vad_params
```

**Reason**: Windows command-line parsing requires proper JSON escaping

### Hybrid Mode Detection

```python
if len(sys.argv) == 1:
    from gooey import Gooey, GooeyParser
    GUI_MODE = True
else:
    from argparse import ArgumentParser as GooeyParser
    def Gooey(*args, **kwargs):
        def decorator(func): return func
        return decorator
    GUI_MODE = False
```

**Effect**: Same code works for both GUI and CLI

---

## File Outputs

### Single File Processing

```
Input: movie.mp4

Outputs:
├── movie_encoded.mkv    (intermediate - video only)
├── movie.srt            (intermediate - subtitles)
└── movie_final.mkv      (FINAL - video + subs)
```

### Batch Processing

```
Input: Folder with episode1.mp4, episode2.mp4

Outputs:
├── episode1_encoded.mkv
├── episode1.srt
├── episode1_final.mkv
├── episode2_encoded.mkv
├── episode2.srt
└── episode2_final.mkv
```

---

## Performance Characteristics

### Stage 1: Video Encoding
- **Time**: 40-80 hours for 2-hour movie (Ryzen 2600)
- **CPU**: 100% utilization (low priority)
- **GPU**: Not used
- **Bottleneck**: CPU speed, preset setting

### Stage 2: Subtitle Generation
- **Time**: ~30 minutes for 2-hour movie
- **GPU (CUDA)**: 5-10x realtime
- **CPU**: 1-2x realtime
- **Bottleneck**: Device speed (GPU >> CPU)

### Stage 3: Muxing
- **Time**: ~1 minute
- **CPU**: Minimal
- **Bottleneck**: Disk I/O

---

## Error Handling

### File Not Found
- Validates input file/folder exists
- Displays error message
- Exits gracefully

### Whisper Failure
- Checks if SRT file was created
- Skips muxing if subtitle generation failed
- Uses encoded video as final output

### Batch Processing Errors
- Tracks failed files separately
- Continues processing remaining files
- Displays summary of successes/failures

---

## Comparison: GUI vs Original CLI

| Feature | main_app.py | pipeline_windows.py |
|---------|-------------|---------------------|
| GUI | ✅ Yes | ❌ No |
| CLI | ✅ Yes | ✅ Yes |
| Batch Folder | ✅ Auto-detect | ❌ Wildcards only |
| Device Choice | ✅ Dropdown | ❌ Hardcoded |
| Standalone .exe | ✅ PyInstaller | ❌ Requires Python |
| VAD Fix | ✅ JSON-escaped | ⚠️ May fail |

---

## Future Enhancements

Potential improvements:

1. **Progress Bar**: Real-time encoding progress
2. **Queue Management**: Pause/resume batch processing
3. **Preset Profiles**: Save/load custom configurations
4. **Multi-threading**: Parallel subtitle generation
5. **Preview**: Quick quality check before full encode
6. **Notifications**: Desktop alerts on completion

---

## References

- **Gooey Documentation**: https://github.com/chriskiehl/Gooey
- **Whisper CTranslate2**: https://github.com/Softcatala/whisper-ctranslate2
- **SVT-AV1**: https://gitlab.com/AOMediaCodec/SVT-AV1
- **PyInstaller**: https://pyinstaller.org/

---

**Last Updated**: 2026-02-05
