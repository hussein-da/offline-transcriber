# Offline Transcriber Examples

This directory contains example audio files and their corresponding transcriptions to demonstrate the capabilities of the Offline Transcriber tool.

## Sample Files

Due to GitHub file size limitations, no large audio files are included in this repository. However, you can use these resources to test the tool:

### Where to get sample audio files

1. **LibriSpeech Dataset**: Free audio book samples
   - [LibriSpeech ASR corpus](https://www.openslr.org/12)
   - Small samples (up to 30s) are ideal for quick testing

2. **Common Voice**: Mozilla's open-source, multi-language voice dataset
   - [Common Voice](https://commonvoice.mozilla.org/en/datasets)

3. **Short test files**: Create your own using the computer's microphone
   - Most operating systems include a voice recorder app
   - Record a short clip and save it as MP3 or WAV

## Example Usage

Once you have an audio file (e.g., `speech.mp3`), transcribe it using:

```bash
transcribe speech.mp3
```

For SRT output:

```bash
transcribe speech.mp3 --formats txt,srt
```

## Expected Output

After transcription, you should see output files like:

- `speech.txt`: Plain text transcription
- `speech.srt`: SRT format with timestamps
- `speech.vtt`: WebVTT format (if requested)
- `speech.json`: JSON format with detailed segment information (if requested)

## Batch Processing

To process multiple files at once:

```bash
transcribe path/to/audio/files --batch --recursive
``` 