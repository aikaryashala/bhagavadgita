# Bhagavad Gita · భగవద్గీత

A bilingual (English / Telugu) web page for **Bhagavad Gita Chapter 18, Verse 78** — featuring the Sanskrit sloka, transliteration, meaning, AI-generated visuals, and an audio practice loop.

**Live site:** https://aikaryashala.com/bhagavadgita/

---

## Features

- Bilingual toggle — switch between English and Telugu instantly
- Full sloka with IAST transliteration
- Meaning in both languages
- Two AI-generated videos: Realistic and Cartoon styles
- Audio practice mode — fullscreen overlay with looping audio recitation
- Graceful stop: finishes the current recitation before exiting
- Open Graph / Twitter Card meta tags for rich link previews when shared

---

## Project Structure

```
bhagavadgita/
├── docs/                        # GitHub Pages root (deployed site)
│   ├── index.html               # Main single-page application
│   ├── .nojekyll                # Disables Jekyll processing on GitHub Pages
│   └── assets/
│       ├── 1_audio.ogg          # Original audio (Ogg Vorbis — source file)
│       ├── 1_audio.mp3          # Converted audio (MP3 — served in browser)
│       ├── realistic_1.mp4      # AI-generated realistic-style video
│       ├── cartoon_1.mp4        # AI-generated cartoon-style video
│       └── og_image.jpeg        # Open Graph preview image (1535x1024)
├── scripts/
│   └── convert_ogg_to_mp3.py   # Audio conversion utility (see below)
└── README.md
```

---

## Audio: OGG vs MP3 vs MP4

### Why does `1_audio.ogg` exist?

The audio recitation was originally recorded and exported in **OGG (Ogg Vorbis)** format. OGG is a free, open-source audio codec developed by the Xiph.Org Foundation. Many recording and editing tools default to OGG because it has no licensing restrictions and delivers excellent quality at low bitrates.

### Why was it converted to `1_audio.mp3`?

Despite being technically superior in some ways, **OGG is not universally supported across browsers**:

| Browser / Platform     | OGG Support | MP3 Support |
|------------------------|-------------|-------------|
| Chrome (desktop)       | Yes         | Yes         |
| Firefox                | Yes         | Yes         |
| Safari (macOS)         | **No**      | Yes         |
| Safari (iOS / iPhone)  | **No**      | Yes         |
| Edge                   | Yes         | Yes         |
| Android WebView        | Yes         | Yes         |

Safari and all browsers on iOS (including Chrome on iPhone, which uses WebKit under the hood) **do not support OGG natively**. Since iOS users represent a significant portion of mobile traffic, serving only OGG would mean those users hear nothing.

**MP3** (MPEG-1 Audio Layer III) has been universally supported across all modern browsers since 2015. It delivers good quality at small file sizes, making it ideal for voice and chant audio delivered over the web.

**Conclusion:** The `.ogg` file is kept as the master/archive copy. The `.mp3` file is what the browser audio player (`<audio>` tag) actually loads and plays.

### What about `.mp4`?

The `.mp4` files (`realistic_1.mp4`, `cartoon_1.mp4`) are **video** files in the MPEG-4 container, encoded with H.264 video. MP4/H.264 is the most widely supported video format across all browsers and devices and requires no conversion. These are served directly via the `<video>` element.

---

## Scripts

### `scripts/convert_ogg_to_mp3.py`

Converts `.ogg` audio files to `.mp3` using `ffmpeg`. Written in Python 3 — no third-party packages required, just a standard Python installation and `ffmpeg` on PATH.

**Requirements:**

- Python 3.6+
- `ffmpeg` installed

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows — download from https://ffmpeg.org/download.html
```

**Single file conversion:**

```bash
python scripts/convert_ogg_to_mp3.py docs/assets/1_audio.ogg docs/assets/1_audio.mp3
```

**Batch conversion** (converts all `.ogg` files in `docs/assets/`):

```bash
python scripts/convert_ogg_to_mp3.py
```

**Audio quality settings used:**
- Encoder: `libmp3lame` (LAME — best open-source MP3 encoder)
- Quality: VBR `-q:a 2` (~190 kbps average, excellent quality)
- Sample rate: 44100 Hz (CD quality)

---

## Deployment

The `docs/` folder is served as a **GitHub Pages** site. The `.nojekyll` file in `docs/` tells GitHub Pages to skip Jekyll processing and serve the files as-is.

The site is also live at the custom domain: **https://aikaryashala.com/bhagavadgita/**

To deploy changes: push commits to the `main` branch. GitHub Pages automatically picks up changes from the `docs/` folder.

---

## Verse Reference

**Bhagavad Gita · Chapter 18, Verse 78**

> *yatra yogeśvaraḥ kṛṣṇo yatra pārtho dhanurdharaḥ*
> *tatra śrīr vijayo bhūtir dhruvā nītir matir mama*

"Wherever there is Krishna, the master of all yoga, and wherever there is Arjuna, the supreme archer — there will surely be fortune, victory, prosperity and unshakeable righteousness. This is my conviction."
