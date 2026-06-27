#!/usr/bin/env python3
"""
convert_ogg_to_mp3.py

PURPOSE
-------
Convert .ogg audio files to .mp3 using ffmpeg.

WHY WE CONVERT OGG -> MP3
--------------------------
The source audio was recorded/exported in OGG (Ogg Vorbis) format, which
is a free and open codec. However, OGG is NOT supported natively in:
  - Safari (macOS / iOS)
  - Older versions of Microsoft Edge

This means a large share of mobile users (all iPhone/iPad users) would get
no audio at all if we served .ogg directly.

MP3 (MPEG-1 Audio Layer III) is supported by 100% of modern browsers
including Chrome, Firefox, Safari, Edge, and all mobile browsers. It also
delivers good quality at small file sizes for voice/chant recordings.

Therefore .mp3 is used as the primary audio format in the player while
the original .ogg file is retained in assets/ for archival purposes.

USAGE
-----
Single file conversion:
    python scripts/convert_ogg_to_mp3.py <input.ogg> [output.mp3]

Batch conversion (converts all .ogg files in docs/assets/):
    python scripts/convert_ogg_to_mp3.py

REQUIREMENTS
------------
ffmpeg must be installed and available on PATH.
    Ubuntu/Debian : sudo apt install ffmpeg
    macOS         : brew install ffmpeg
    Windows       : https://ffmpeg.org/download.html

AUDIO QUALITY SETTINGS USED
-----------------------------
  -codec:a libmp3lame   -- LAME MP3 encoder (best quality)
  -q:a 2                -- VBR quality 2 (~190 kbps average, excellent)
  -ar 44100             -- sample rate 44.1 kHz (CD quality)
"""

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ASSETS_DIR  = PROJECT_ROOT / "docs" / "assets"

FFMPEG_ARGS = [
    "-codec:a", "libmp3lame",
    "-q:a", "2",
    "-ar", "44100",
]


def check_ffmpeg() -> None:
    """Verify ffmpeg is installed and reachable."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except FileNotFoundError:
        sys.exit(
            "[convert] ERROR: ffmpeg not found. "
            "Install it first (see script header)."
        )


def convert(input_path: Path, output_path: Path) -> None:
    """Convert a single .ogg file to .mp3."""
    if not input_path.is_file():
        sys.exit(f"[convert] ERROR: Input file not found: {input_path}")

    if output_path.exists():
        print(f"[convert] WARNING: Overwriting existing file: {output_path.name}")

    print(f"[convert] Converting: {input_path.name} -> {output_path.name}")

    cmd = ["ffmpeg", "-y", "-i", str(input_path)] + FFMPEG_ARGS + [str(output_path), "-loglevel", "warning"]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        sys.exit(f"[convert] ERROR: ffmpeg failed for {input_path.name}")

    print(f"[convert] Done: {output_path}")


def batch_convert() -> None:
    """Convert all .ogg files found in docs/assets/."""
    print(f"[convert] Batch mode — scanning: {ASSETS_DIR}")

    ogg_files = sorted(ASSETS_DIR.glob("*.ogg"))

    if not ogg_files:
        sys.exit(f"[convert] ERROR: No .ogg files found in {ASSETS_DIR}")

    for ogg_file in ogg_files:
        mp3_file = ogg_file.with_suffix(".mp3")
        convert(ogg_file, mp3_file)

    print(f"[convert] Batch complete. Converted {len(ogg_files)} file(s).")


def main() -> None:
    check_ffmpeg()

    if len(sys.argv) >= 2:
        # Single-file mode
        input_path  = Path(sys.argv[1])
        output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else input_path.with_suffix(".mp3")
        convert(input_path, output_path)
    else:
        # Batch mode
        batch_convert()


if __name__ == "__main__":
    main()
