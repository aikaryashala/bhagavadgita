#!/usr/bin/env bash
# =============================================================================
# convert_ogg_to_mp3.sh
#
# PURPOSE
#   Convert .ogg audio files to .mp3 using ffmpeg.
#
# WHY WE CONVERT OGG -> MP3
#   The source audio was recorded/exported in OGG (Ogg Vorbis) format, which
#   is a free and open codec. However, OGG is NOT supported natively in:
#     - Safari (macOS / iOS)
#     - Older versions of Microsoft Edge
#   This means a large share of mobile users (all iPhone/iPad users) would get
#   no audio at all if we served .ogg directly.
#
#   MP3 (MPEG-1 Audio Layer III) is supported by 100% of modern browsers
#   including Chrome, Firefox, Safari, Edge, and all mobile browsers. It also
#   delivers good quality at small file sizes for voice/chant recordings.
#
#   Therefore .mp3 is used as the primary audio format in the player while
#   the original .ogg file is retained in assets/ for archival purposes.
#
# USAGE
#   Single file conversion:
#     ./scripts/convert_ogg_to_mp3.sh <input.ogg> [output.mp3]
#
#   Batch conversion (converts all .ogg files in docs/assets/):
#     ./scripts/convert_ogg_to_mp3.sh
#
# REQUIREMENTS
#   ffmpeg must be installed.
#     Ubuntu/Debian : sudo apt install ffmpeg
#     macOS         : brew install ffmpeg
#     Windows       : https://ffmpeg.org/download.html
#
# AUDIO QUALITY SETTINGS USED
#   -codec:a libmp3lame   -- use the LAME MP3 encoder (best quality)
#   -q:a 2                -- VBR quality 2 (~190 kbps average, excellent)
#   -ar 44100             -- sample rate 44.1 kHz (CD quality)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSETS_DIR="$PROJECT_ROOT/docs/assets"

# ---- Helpers ----------------------------------------------------------------

log()  { echo "[convert] $*"; }
warn() { echo "[convert] WARNING: $*" >&2; }
die()  { echo "[convert] ERROR: $*" >&2; exit 1; }

check_ffmpeg() {
  command -v ffmpeg &>/dev/null || die "ffmpeg not found. Install it first (see script header)."
}

convert_file() {
  local input="$1"
  local output="${2:-${input%.ogg}.mp3}"

  [[ -f "$input" ]] || die "Input file not found: $input"

  if [[ -f "$output" ]]; then
    warn "Output already exists, overwriting: $output"
  fi

  log "Converting: $(basename "$input") -> $(basename "$output")"
  ffmpeg -y -i "$input" \
    -codec:a libmp3lame \
    -q:a 2 \
    -ar 44100 \
    "$output" \
    -loglevel warning

  log "Done: $output"
}

# ---- Main -------------------------------------------------------------------

check_ffmpeg

if [[ $# -ge 1 ]]; then
  # Single-file mode: ./convert_ogg_to_mp3.sh input.ogg [output.mp3]
  INPUT="$1"
  OUTPUT="${2:-${INPUT%.ogg}.mp3}"
  convert_file "$INPUT" "$OUTPUT"
else
  # Batch mode: convert all .ogg files in docs/assets/
  log "Batch mode — scanning: $ASSETS_DIR"
  OGG_FILES=( "$ASSETS_DIR"/*.ogg )

  if [[ ! -f "${OGG_FILES[0]}" ]]; then
    die "No .ogg files found in $ASSETS_DIR"
  fi

  COUNT=0
  for ogg_file in "${OGG_FILES[@]}"; do
    mp3_file="${ogg_file%.ogg}.mp3"
    convert_file "$ogg_file" "$mp3_file"
    (( COUNT++ ))
  done

  log "Batch complete. Converted $COUNT file(s)."
fi
