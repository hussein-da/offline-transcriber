#!/usr/bin/env python3
"""
Example script demonstrating the programmatic use of the offline_transcriber package.
This shows how to integrate the transcription functionality directly into your own Python scripts.
"""

import os
import sys
from pathlib import Path

from offline_transcriber.audio import process_audio_file, cleanup_temp_file
from offline_transcriber.transcriber import WhisperTranscriber
from offline_transcriber.postprocessor import save_transcription

def main():
    # Check for command line argument (audio file path)
    if len(sys.argv) < 2:
        print("Usage: python basic_transcription.py /path/to/audiofile.mp3")
        return 1
    
    # Get audio file path from command line
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"Error: File '{audio_path}' does not exist.")
        return 1
    
    print(f"Processing: {audio_path}")
    
    try:
        # Process audio file (convert, resample, etc.)
        audio_array, temp_file = process_audio_file(audio_path)
        
        # Initialize transcriber with the chosen model
        # Options: tiny, base, small, medium, large
        transcriber = WhisperTranscriber(model_name="small")
        
        # Transcribe the audio (language=None for auto-detection)
        result = transcriber.transcribe(
            audio_array,
            language=None,  # Auto-detect language
            task="transcribe"  # Or "translate" to translate to English
        )
        
        # Clean up temporary files
        cleanup_temp_file(temp_file)
        
        # Define output path (same as input but with .txt extension)
        output_path = os.path.splitext(audio_path)[0]
        
        # Save transcription to output file(s)
        output_files = save_transcription(
            result,
            output_path,
            formats=["txt"]  # Options: txt, srt, vtt, json
        )
        
        print(f"Transcription complete!")
        print(f"Detected language: {result.language}")
        
        # Print paths to all output files
        for fmt, path in output_files.items():
            print(f"Output {fmt.upper()}: {path}")
            
        # Print a sample of the transcription
        with open(output_files['txt'], 'r', encoding='utf-8') as f:
            text = f.read(200)  # First 200 characters
            print(f"\nSample transcription:\n{text}...")
        
        return 0
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 