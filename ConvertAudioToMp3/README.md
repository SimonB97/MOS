# Audio Converter

Simple script to convert audio files (FLAC, WAV, M4A) to MP3 format using ffmpeg.

## Requirements

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) installed
- ffmpeg installed (see installation instructions below)

## Installing ffmpeg

Windows:
```bash
winget install ffmpeg
```

macOS:
```bash
brew install ffmpeg
```

Linux:
```bash
sudo apt install ffmpeg
```

## Usage


Basic usage:
```bash
uv run mp3.py input_folder -o output_folder
```

With custom number of parallel workers:
```bash
uv run mp3.py input_folder -o output_folder -w 4
```

Show help:
```bash
uv run mp3.py -h
```

**Note:** When using `uv`, you can replace `mp3.py` with the path to the script in this repository, e.g.: 
```bash
uv run https://raw.githubusercontent.com/SimonB97/my-open-scripts/main/ConvertAudioToMp3/mp3.py input_folder -o output_folder
```

## Features

- Converts FLAC, WAV, and M4A to MP3
- Preserves folder structure while converting directories recursively
- Parallel processing (default: 50% of CPU cores)