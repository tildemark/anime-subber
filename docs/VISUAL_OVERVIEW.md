# 📊 Visual Overview of Your Scripts

> **Note:** All Python scripts are located in the `scripts/` folder. Use wrapper scripts in `wrappers/ps1/` (Windows) or `wrappers/sh/` (Linux/macOS) for simplified execution.

## Script Ecosystem Map

```
                     🎬 ANIME SUBBER TOOLKIT 🎬
                    ┌────────────────────────────┐
                    │    7 Python Scripts        │
                    │    3 Decision Points       │
                    │    1 Perfect Workflow      │
                    └────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────────┐  ┌────────────┐  ┌──────────────┐
        │   ENCODING   │  │  BENCHMARK │  │  SUBTITLES   │
        │   SCRIPTS    │  │   SCRIPTS  │  │   SCRIPTS    │
        └──────────────┘  └────────────┘  └──────────────┘
             │                 │                │
        ┌────┴────┬────┐       │          ┌─────┴─────┐
        │          │    │       │          │           │
        ▼          ▼    ▼       ▼          ▼           ▼
encode_simple  encode_smart  benchmark  pipeline_*   add_subtitles
    BASIC      ⭐SMART      QUICK      FULL PIPE      SUBS ONLY
    FAST       INTERACTIVE TEST       video+subs     (existing video)
    SIMPLE     ✓BENCHMARK  ≈2min      (Windows/Unix)
               PREVIEW
               ≈40-80h
```

---

## Decision Flowchart (Detailed)

```
                        START HERE
                           │
                    What do you need?
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   VIDEO ONLY      VIDEO + SUBS         SUBS ONLY
        │                  │                  │
        │           (BEST CHOICE)            │
        │                  │                  │
   Do you want    ─────────────────   I already have
   to test first?      YES│NO        encoded video
        │                  │                  │
       YES│              NO│               YES│
        │                  │                  │
        ▼                  ▼                  ▼
    bench.py     auto_anime_win.py    translate_only.py
    (2 min)      (Windows)             (~30 min)
         │        -or-                    │
         │        auto_anime_unix.py      │
         │        (Linux/macOS)           │
         │                                │
         └────────────┬───────────────────┘
                      │
                      ▼
                 ✅ DONE
             (Final MKV file)
```

---

## Timeline: What Happens When

### Using convert2.py or auto_anime_win.py

```
Timeline for ~2 hour anime episode (Ryzen 2600):

Start
  │
  ├─ [Immediate] Parse arguments & validate input
  │
  ├─ [If convert2.py] Benchmark 4 options (~2 minutes)
  │                   └─ Test 8-second clips of each preset
  │
  ├─ [User input] Pick your settings (convert2.py only)
  │
  ├─ [~46-68 hours] ▓▓▓▓▓ VIDEO ENCODING ▓▓▓▓▓
  │                 ffmpeg + libsvtav1 encoding
  │                 (90% of total time)
  │
  ├─ [~5 minutes] ▓▓ SUBTITLE GENERATION ▓▓
  │               Whisper AI transcription
  │               (10% of total time)
  │
  ├─ [< 1 minute] ▓ MUXING ▓
  │               Combine video + subtitles
  │
  └─ ✅ COMPLETE
        Final output file ready
```

---

## Script Comparison Matrix

### Core Differences

```
Feature          │ convert.py │ convert2.py │ auto_anime │ translate_only
─────────────────┼────────────┼─────────────┼───────────┼────────────────
Encodes video    │     ✓      │      ✓      │     ✓     │       ✗
Generates subs   │     ✗      │      ✗      │     ✓     │       ✓
Muxes together   │     ✗      │      ✗      │     ✓     │       ✓
Benchmarks first │     ✗      │      ✓      │     ✗     │       ✗
Interactive menu │     ✗      │      ✓      │     ✗     │       ✗
Auto-shutdown    │     ✗      │      ✓      │     ✓     │       ✗
Fixed settings   │     ✓      │     (user)  │   (user)  │       N/A
Time to start    │    Fast    │   2 min     │    Fast   │      Fast
Total time       │  40-80 hrs │  40-80 hrs  │  40-80 hrs│     ~30 min
One-command      │     ✓      │     ✓      │     ✓     │       ✓
Windows support  │     ✓      │     ✓      │     ✓     │       ✓
Linux support    │     ✓      │     ✓      │     ✓     │       ✗
```

---

## Speed Comparison (Ryzen 2600)

```
Option                          Encoding Time    File Size     Best For
────────────────────────────────────────────────────────────────────────
1. 1080p + P6 + CRF30          68.5 hours       1.2 GB        ⭐ Highest quality
2. 1080p + P8 + CRF36          45.2 hours       1.5 GB        Best balance
3. 720p + P8 + CRF32           32.1 hours       0.8 GB        Good quality
4. 720p + P10 + CRF40          18.7 hours       0.6 GB        ⚡ Fastest

Source material: 5.8 GB
Duration: ~120 minutes (2-hour movie)
```

---

## File Size Scaling Formula

```
                    Base Factor: 0.17 @ CRF 30

Actual Size = Source GB × [0.17 × 2^((CRF-30)/10)] × [720p multiplier]

Examples for 5.8 GB source:

CRF 30 (default):  5.8 × 0.17 = 1.0 GB
CRF 36 (more comp): 5.8 × 0.25 = 1.5 GB  (each +10 ~= 50% more data)
CRF 40 (extreme):  5.8 × 0.35 = 2.0 GB

With 720p scaling applied (×0.6):
CRF 30 @ 720p:     5.8 × 0.17 × 0.6 = 0.6 GB
CRF 40 @ 720p:     5.8 × 0.35 × 0.6 = 1.2 GB
```

---

## Execution Stages Breakdown

### convert.py / convert_v1.py
```
Input Video
    │
    ├─ [Parse arguments]
    ├─ [Build ffmpeg command]
    ├─ [⏳ ~40-80 hours] Video encoding
    │   └─ Audio: Opus 128k
    │   └─ Video: AV1 (SVT-AV1)
    └─ Output MKV file
```

### convert2.py
```
Input Video
    │
    ├─ [Parse arguments]
    ├─ [⏳ ~2 minutes] Benchmark 4 presets
    │   ├─ P6/CRF30 @ source resolution
    │   ├─ P8/CRF36 @ source resolution  
    │   ├─ P8/CRF32 @ 720p
    │   └─ P10/CRF40 @ 720p
    ├─ [User input] Pick option (1-4)
    ├─ [⏳ ~40-80 hours] Full video encoding
    └─ Output MKV file
```

### auto_anime_win.py / auto_anime_unix.py
```
Input Video
    │
    ├─ [Parse arguments]
    │
    ├─ STAGE 1: Video Encoding (⏳ ~40-80 hours)
    │   ├─ Build ffmpeg command
    │   ├─ Apply scaling filter (if specified)
    │   ├─ Encode to AV1 (SVT-AV1)
    │   └─ Audio to Opus 128k
    │   Output: intermediate.mkv
    │
    ├─ STAGE 2: Subtitle Generation (⏳ ~20 minutes)
    │   ├─ Extract audio
    │   ├─ Transcribe Japanese audio (Whisper)
    │   ├─ Translate to English
    │   └─ Save as SRT subtitles
    │   Output: input_basename.srt
    │
    ├─ STAGE 3: Muxing (⏳ <1 minute)
    │   ├─ Read MKV + SRT files
    │   ├─ Copy streams (no re-encoding)
    │   ├─ Add subtitle track
    │   └─ Add metadata (language=eng)
    │   Output: final_output.mkv
    │
    └─ [Optional] Auto-shutdown (Windows only)
```

### translate_only.py
```
Input Video (already encoded)
    │
    ├─ [Parse arguments]
    │
    ├─ STAGE 1: Subtitle Generation (⏳ ~20 minutes)
    │   ├─ Extract audio
    │   ├─ Transcribe Japanese audio (Whisper)
    │   ├─ Translate to English (Medium model)
    │   └─ Save as SRT subtitles
    │   Output: input_basename.srt
    │
    ├─ STAGE 2: Muxing (⏳ <1 minute)
    │   ├─ Read video + SRT files
    │   ├─ Copy video (no re-encoding)
    │   ├─ Add subtitle track
    │   └─ Add metadata
    │   Output: final_output.mkv
    │
    └─ ✅ Done
```

---

## Preset Strength Explanation

```
Preset 0 (Slowest):      ▓▓▓▓▓▓▓▓▓▓ 100% time  │  Best quality
         1:               ▓▓▓▓▓▓▓▓░░  82% time  │
         2:               ▓▓▓▓▓▓░░░░  71% time  │
         3:               ▓▓▓▓▓░░░░░  61% time  │  ⭐ High quality
         4:               ▓▓▓▓░░░░░░  54% time  │
         5:               ▓▓▓░░░░░░░  47% time  │  Good tradeoff
         6:               ▓▓░░░░░░░░  41% time  │
         7:               ▓░░░░░░░░░  35% time  │  Recommended
         8:               ░░░░░░░░░░  30% time  │  Default
         9:                           23% time  │  Fast
Preset 10 (Fastest):                 18% time  │  Acceptable quality
```

---

## Which to Pick for Your Use Case?

```
┌─────────────────────────────────────────────────────────┐
│ SCENARIO              │ SCRIPT      │ SETTINGS           │
├─────────────────────────────────────────────────────────┤
│ "Just do it, fast"    │ convert.py  │ (fixed: P8/CRF30) │
│ "Show me options"     │ convert2.py │ (interactive)     │
│ "Quality first"       │ auto_anime  │ source/P6/CRF30   │
│ "Fast + subs"         │ auto_anime  │ 720p/P8/CRF36     │
│ "Already have video"  │ translate   │ (subs only)       │
│ "Test my hardware"    │ bench.py    │ (estimates)       │
└─────────────────────────────────────────────────────────┘
```

---

## Resource Usage During Encoding

```
                During Video Encoding      During Subtitle Generation
                ─────────────────────      ──────────────────────────

CPU Usage:      ▓▓▓▓▓▓▓▓▓▓ 70-90%         ░░░░░░░░░░ 10-20%
GPU Usage:      ░░░░░░░░░░ 0%             ▓▓▓▓▓▓▓▓░░ 60-80%
RAM Usage:      ▓▓░░░░░░░░ 2-3 GB        ▓▓▓▓░░░░░░ 4-6 GB
Disk I/O:       ▓▓▓▓░░░░░░ Medium         ░░░░░░░░░░ None

Your system is:
┌─────────────────────────────────┐
│ Ryzen 2600 (12-core CPU)       │ ← Video encoding bottleneck
│ GTX 1050 (2GB VRAM)            │ ← Subtitle generation (good)
│ 16 GB RAM                       │ ← Plenty
│ SSD Storage                      │ ← Good I/O
└─────────────────────────────────┘

Limiting Factor: CPU (Ryzen 2600 is mid-range)
Video encoding ~40-80 hours is expected
```

---

**See SCRIPT_COMPARISON.md for complete details**
**See QUICKSTART.md for quick reference**
