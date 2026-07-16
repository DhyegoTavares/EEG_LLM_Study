# EEG LLM Study 
Experiment Google Sheets: https://docs.google.com/spreadsheets/d/1HTe9ypY4oCW17veFPoG8ExAGW-UyXvtm-LfxjTfTPjs/edit?usp=sharing

Experiment Google Form: https://forms.gle/nGVjgxEaLVqSGaeZ6

## Audio Transcription

Offline audio transcription pipeline for the EEG & LLM study. Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) with the `large-v3-turbo` model, running on GPU (NVIDIA CUDA) with automatic CPU fallback.

## Requirements

- Python 3.10+
- NVIDIA GPU with CUDA 12 (optional — CPU fallback is available)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

pip install faster-whisper nvidia-cublas-cu12 nvidia-cudnn-cu12
```

## Usage

Place audio files in the `Audios/` folder and run:

```bash
python Audios\transcription.py
```

This processes every supported file in `Audios/` and saves a `.txt` transcript next to each audio file.

### Options

| Argument | Default | Description |
|---|---|---|
| `path` | `Audios/` | Path to a single audio file or a directory |
| `--model` | `large-v3-turbo` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`, `large-v3-turbo`) |
| `--language` | `pt` | Language code (`pt`, `en`, `es`, …) or `auto` for detection |
| `--format` | `txt` | Output format: `txt`, `srt`, or `vtt` |
| `--beam-size` | `5` | Beam size — higher is more accurate but slower |
| `--cpu` | off | Force CPU inference |
| `--batch` | auto | Process all files in a directory (enabled automatically when a directory is passed) |

### Examples

```bash
# Transcribe a single file
python Audios\transcription.py Audios/session1.mp4

# Use English and output subtitles
python Audios\transcription.py Audios/session1.mp4 --language en --format srt

# Run on CPU only
python Audios\transcription.py --cpu

# Use a larger model for higher accuracy
python Audios\transcription.py --model large-v3
```

## Supported Formats

`.mp3` `.wav` `.m4a` `.flac` `.ogg` `.wma` `.aac` `.mp4` `.mkv`

## Output

Transcripts are saved in the same directory as the source audio file, with the same name and the chosen extension (`.txt` by default).

```
Audios/
├── session1.mp4
├── session1.txt   ← generated
├── session2.mp4
└── session2.txt   ← generated
```

## Troubleshooting

**`cublas64_12.dll` not found** — CUDA libraries are installed but Windows cannot locate them. The script handles this automatically via `os.add_dll_directory`. If the error persists, reinstall:
```bash
pip install --force-reinstall nvidia-cublas-cu12 nvidia-cudnn-cu12
```

**Slow transcription** — The script falls back to CPU when GPU initialization fails. Check that your NVIDIA drivers support CUDA 12.
