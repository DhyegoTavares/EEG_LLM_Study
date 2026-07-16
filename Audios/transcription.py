#!/usr/bin/env python3
"""
Audio transcription script using faster-whisper (large-v3-turbo).
Optimized for NVIDIA GPUs; falls back to CPU automatically.

Usage:
    python transcription.py
    python transcription.py audio.mp3
    python transcription.py audio.mp3 --language en
    python transcription.py audio.mp3 --format srt
    python transcription.py Audios/ --batch
    python transcription.py audio.mp3 --model large-v3 --cpu
"""

import argparse
import os
import sys
import time
from pathlib import Path

SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma", ".aac", ".mp4", ".mkv"}
DEFAULT_AUDIO_DIR = Path(__file__).parent / "Audios"


def _register_nvidia_dlls():
    """On Windows, add nvidia-*-cu12 DLL directories to the search path."""
    if sys.platform != "win32":
        return
    for path in sys.path:
        nvidia_dir = Path(path) / "nvidia"
        if nvidia_dir.is_dir():
            for subpkg in nvidia_dir.iterdir():
                bin_dir = subpkg / "bin"
                if bin_dir.is_dir():
                    os.add_dll_directory(str(bin_dir))


_register_nvidia_dlls()


def check_dependencies():
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        print("ERROR: faster-whisper is not installed.")
        print("Install with: pip install faster-whisper")
        sys.exit(1)


def load_model(model_name: str, force_cpu: bool):
    from faster_whisper import WhisperModel

    if force_cpu:
        print(f"Loading model '{model_name}' on CPU (int8)...")
        return WhisperModel(model_name, device="cpu", compute_type="int8")

    try:
        print(f"Loading model '{model_name}' on GPU (float16)...")
        return WhisperModel(model_name, device="cuda", compute_type="float16")
    except Exception as e:
        print(f"Warning: failed to load model on GPU ({e}).")
        print("Make sure NVIDIA drivers and cuDNN are installed:")
        print("  pip install nvidia-cudnn-cu12 nvidia-cublas-cu12")
        print("Falling back to CPU (slower)...")
        return WhisperModel(model_name, device="cpu", compute_type="int8")


def format_srt_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def transcribe_file(model, audio_path: Path, language: str, output_format: str, beam_size: int):
    print(f"\n{'='*60}")
    print(f"Transcribing: {audio_path.name}")
    print(f"{'='*60}")

    start = time.time()

    segments, info = model.transcribe(
        str(audio_path),
        language=language if language != "auto" else None,
        beam_size=beam_size,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    print(f"Detected language: {info.language} (confidence: {info.language_probability:.2%})")
    print(f"Audio duration: {info.duration:.1f}s")
    print("Processing segments...\n")

    segments_list = []
    full_text = []

    for segment in segments:
        text = segment.text.strip()
        segments_list.append(segment)
        full_text.append(text)
        print(f"[{segment.start:7.2f}s -> {segment.end:7.2f}s] {text}")

    elapsed = time.time() - start
    speed = info.duration / elapsed if elapsed > 0 else 0

    print(f"\nDone in {elapsed:.1f}s (speed: {speed:.1f}x real time)")

    output_path = audio_path.with_suffix(f".{output_format}")

    if output_format == "txt":
        output_path.write_text("\n".join(full_text), encoding="utf-8")
    elif output_format == "srt":
        with open(output_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments_list, start=1):
                f.write(f"{i}\n")
                f.write(f"{format_srt_timestamp(seg.start)} --> {format_srt_timestamp(seg.end)}\n")
                f.write(f"{seg.text.strip()}\n\n")
    elif output_format == "vtt":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for seg in segments_list:
                start_vtt = format_srt_timestamp(seg.start).replace(",", ".")
                end_vtt = format_srt_timestamp(seg.end).replace(",", ".")
                f.write(f"{start_vtt} --> {end_vtt}\n")
                f.write(f"{seg.text.strip()}\n\n")

    print(f"Saved to: {output_path}")
    return output_path


def collect_files(path: Path, batch: bool) -> list[Path]:
    if batch:
        if not path.is_dir():
            print(f"ERROR: '{path}' is not a valid directory.")
            sys.exit(1)
        files = sorted(p for p in path.iterdir() if p.suffix.lower() in SUPPORTED_FORMATS)
        if not files:
            print(f"No supported audio files found in '{path}'.")
            sys.exit(1)
        return files
    else:
        if not path.is_file():
            print(f"ERROR: file '{path}' not found.")
            sys.exit(1)
        if path.suffix.lower() not in SUPPORTED_FORMATS:
            print(f"Warning: unusual extension '{path.suffix}', attempting to process anyway.")
        return [path]


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio locally using faster-whisper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "path", type=str, nargs="?", default=None,
        help=f"Path to an audio file or directory. Default: {DEFAULT_AUDIO_DIR}",
    )
    parser.add_argument(
        "--model", type=str, default="large-v3-turbo",
        help="Model to use (tiny, base, small, medium, large-v3, large-v3-turbo). Default: large-v3-turbo",
    )
    parser.add_argument(
        "--language", type=str, default="pt",
        help="Language code (pt, en, es, etc.) or 'auto' for automatic detection. Default: pt",
    )
    parser.add_argument(
        "--format", type=str, default="txt", choices=["txt", "srt", "vtt"],
        help="Output format: txt, srt (subtitles), or vtt. Default: txt",
    )
    parser.add_argument(
        "--beam-size", type=int, default=5,
        help="Beam size (higher = more accurate but slower). Default: 5",
    )
    parser.add_argument("--cpu", action="store_true", help="Force CPU instead of GPU")
    parser.add_argument("--batch", action="store_true", help="Process all audio files in a directory")

    args = parser.parse_args()

    check_dependencies()

    path = Path(args.path) if args.path else DEFAULT_AUDIO_DIR
    batch = args.batch or path.is_dir()
    files = collect_files(path, batch)

    print(f"Files to process: {len(files)}")

    model = load_model(args.model, args.cpu)

    for file in files:
        try:
            transcribe_file(model, file, args.language, args.format, args.beam_size)
        except Exception as e:
            print(f"ERROR processing '{file.name}': {e}")
            continue

    print(f"\n{'='*60}")
    print("Processing complete.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
