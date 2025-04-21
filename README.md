# Offline Transcriber

A simple, CLI-based transcription tool for audio files that works 100% offline, with no internet connection or APIs required.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

## Project Information

**Author:** Hussein Daoud  
**GitHub:** [hussein-da](https://github.com/hussein-da)

> This project is a personal/hobby project and is not intended for commercial use. It was developed as a concept to potentially extend my [note-ai-assistant](https://github.com/hussein-da/note-ai-assistant) project and reduce operational costs by moving transcription processing offline. I'm open to collaboration and discussions about scaling and deployment opportunities. Feel free to contact me through GitHub for any inquiries!

## Features

- 🎤 **Transcribe any audio file** - Support for WAV, MP3, FLAC, AAC, and more
- 🌐 **100% offline** - No internet connection or API keys required
- 🔊 **Multiple languages** - Automatic language detection or manual selection
- 📁 **Batch processing** - Process entire directories at once
- 📝 **Multiple output formats** - Text, SRT, WebVTT, or JSON
- 🔄 **Translation** - Can translate any language to English

## Installation

### Prerequisites

- Python 3.8+
- FFmpeg (required for audio processing)

### Installation via pip

```bash
# Install from source in development mode
git clone https://github.com/hussein-da/offline-transcriber.git
cd offline-transcriber
pip install -e .
```

### Installing FFmpeg

FFmpeg is required for audio processing. Use our setup script to install it easily:

#### Windows
Run PowerShell as Administrator and execute:
```powershell
.\setup_ffmpeg.ps1
```

#### Other platforms
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

## Quick Start Guide

### 1. Place audio files in the audio directory

```bash
# Just copy your audio files to the audio/ directory
# Example: copy "C:\path\to\your\audio.mp3" audio\
```

### 2. Transcribe your audio

```bash
# Just provide the filename if it's in the audio/ directory
transcribe audio/your-audio-file.mp3
```

## Usage

### Basic Usage

```bash
transcribe path/to/audio.mp3
```

### Command Line Options

```
transcribe [-h] [-m {tiny,base,small,medium,large}] [-o OUTPUT]
           [-f FORMATS] [-l LANGUAGE] [-t {transcribe,translate}]
           [-b] [-r] [-d DEVICE] [-v] [--version]
           input
```

#### Arguments

- `input`: Input audio file or directory

#### Options

- `-h, --help`: Show help message and exit
- `-m, --model {tiny,base,small,medium,large}`: Whisper model size to use (default: small)
- `-o, --output OUTPUT`: Output file path without extension (default: same as input)
- `-f, --formats FORMATS`: Output formats as comma-separated list (default: txt)
- `-l, --language LANGUAGE`: Language code or "auto" for auto-detection (default: auto)
- `-t, --task {transcribe,translate}`: Task to perform (default: transcribe)
- `-b, --batch`: Process all audio files in the input directory
- `-r, --recursive`: Recursively process subdirectories (only with --batch)
- `-d, --device DEVICE`: Device to use (cpu, cuda, cuda:0, etc.)
- `-v, --verbose`: Increase output verbosity
- `--version`: Show version and exit

### Examples

#### Transcribe with specific model and output format:

```bash
transcribe audio/lecture.mp3 --model medium --formats txt,srt
```

#### Batch process a directory:

```bash
transcribe audio/ --batch
```

#### Translate to English:

```bash
transcribe audio/interview_german.mp3 --task translate
```

#### Specify language (instead of auto-detection):

```bash
transcribe audio/speech.mp3 --language en
```

## Architecture and Workflow

The Offline Transcriber is built with a modular architecture that separates concerns and allows for easy extension:

### Core Components

1. **Transcriber Module** (`transcriber.py`): 
   - The heart of the system that interfaces with OpenAI's Whisper model
   - Handles model loading, language detection, and the actual transcription process
   - Provides the `WhisperTranscriber` class that manages the full transcription lifecycle

2. **Audio Processing Module** (`audio.py`):
   - Handles loading and preprocessing of audio files
   - Performs format conversion, resampling, and normalization
   - Creates temporary files for processing and cleans them up afterward

3. **Postprocessor Module** (`postprocessor.py`):
   - Converts transcription results to various output formats (TXT, SRT, WebVTT, JSON)
   - Handles timestamp formatting and segment arrangement
   - Manages file saving operations

4. **Command Line Interface** (`cli.py`):
   - Provides the user-facing CLI interface
   - Processes command-line arguments and options
   - Orchestrates the workflow between components

### Data Flow & Processing Pipeline

The typical transcription workflow follows these steps:

1. **Input Parsing**: The CLI parses the input file path and options.
2. **Audio Loading**: The audio file is loaded and converted to a compatible format.
3. **Preprocessing**: Audio is resampled to 16kHz, converted to mono if needed.
4. **Model Loading**: The Whisper model is loaded based on the selected size.
5. **Transcription**: The audio is processed through the model for transcription.
6. **Postprocessing**: The results are formatted according to the requested output formats.
7. **Output**: Transcription files are saved to disk.

## Project Structure

```
offline-transcriber/
├── audio/                     # Place your audio files here
│   └── README.md              # Instructions for audio files
├── src/                       # Source code
│   └── offline_transcriber/   # Main package
│       ├── __init__.py        # Package version and metadata
│       ├── audio.py           # Audio preprocessing functions
│       ├── cli.py             # Command-line interface
│       ├── postprocessor.py   # Output formatting and saving
│       └── transcriber.py     # Whisper model interface
├── tests/                     # Unit tests
├── setup_ffmpeg.ps1           # FFmpeg installation script for Windows
├── setup.py                   # Package setup
└── README.md                  # This file
```

## Understanding Whisper Models

| Model | Size | Memory Required | Relative Speed | Accuracy |
|-------|------|-----------------|----------------|----------|
| tiny  | 39M  | ~1GB            | ~32x           | Basic    |
| base  | 74M  | ~1GB            | ~16x           | Good     |
| small | 244M | ~2GB            | ~6x            | Better   |
| medium| 769M | ~5GB            | ~2x            | Great    |
| large | 1.5G | ~10GB           | 1x (Slowest)   | Best     |

Choose the model based on your hardware constraints and accuracy needs.

## Requirements

- numpy
- pydub
- openai-whisper
- tqdm
- FFmpeg (external dependency)

## Troubleshooting

### FFmpeg not found

If you see errors like:
```
RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
```

Run the FFmpeg setup script:
```
.\setup_ffmpeg.ps1
```

### Audio file not found

Make sure the audio file exists and is accessible. For simplicity, copy your audio files to the `audio/` directory.

## Relation to note-ai-assistant

This tool was developed as a complementary component to my [note-ai-assistant](https://github.com/hussein-da/note-ai-assistant) project. While note-ai-assistant provides a complete meeting transcription and analysis solution with a web interface, this tool focuses specifically on the offline transcription aspect, which could potentially reduce dependency on external APIs and lower operational costs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 