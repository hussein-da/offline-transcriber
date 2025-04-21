# Audio Files Directory

This directory is intended for storing audio files that you want to transcribe using the Offline Transcriber tool.

## Supported File Formats

The transcriber supports the following audio file formats:
- MP3 (`.mp3`)
- WAV (`.wav`)
- FLAC (`.flac`)
- AAC (`.aac`)
- M4A (`.m4a`)
- OGG (`.ogg`)

## Usage

1. **Place your audio files in this directory**
   ```
   # Example (Windows)
   copy "C:\path\to\your\recording.mp3" audio\
   
   # Example (Unix)
   cp /path/to/your/recording.mp3 audio/
   ```

2. **Transcribe files directly using the relative path**
   ```
   transcribe audio/recording.mp3
   ```

3. **Batch process all files in this directory**
   ```
   transcribe audio/ --batch
   ```

## Best Practices

- Keep your audio files organized by creating subdirectories for different projects or categories
- Use meaningful file names for easy reference
- For large audio files, consider using the `--model tiny` or `--model base` options for faster processing
- For better accuracy with important files, use `--model medium` or `--model large`

## Output Files

By default, transcription output files will be created in this same directory with the same base name as your audio file but with different extensions:

- `recording.mp3` → `recording.txt` (default)
- If you specify other formats: `recording.srt`, `recording.vtt`, `recording.json`

To change the output location, use the `--output` option:
```
transcribe audio/recording.mp3 --output path/to/output/transcript
``` 