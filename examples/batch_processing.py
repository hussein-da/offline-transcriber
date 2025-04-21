#!/usr/bin/env python3
"""
Example script demonstrating batch processing of multiple audio files.
This shows how to implement a custom batch processor with progress tracking.
"""

import os
import glob
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any

from tqdm import tqdm

from offline_transcriber.audio import process_audio_file, cleanup_temp_file
from offline_transcriber.transcriber import WhisperTranscriber
from offline_transcriber.postprocessor import save_transcription

def find_audio_files(directory: str, recursive: bool = False) -> List[str]:
    """Find all audio files in a directory."""
    extensions = ["*.wav", "*.mp3", "*.flac", "*.aac", "*.ogg", "*.m4a"]
    audio_files = []
    
    # Build pattern based on whether we want recursive search
    if recursive:
        for ext in extensions:
            pattern = os.path.join(directory, "**", ext)
            audio_files.extend(glob.glob(pattern, recursive=True))
    else:
        for ext in extensions:
            pattern = os.path.join(directory, ext)
            audio_files.extend(glob.glob(pattern))
    
    return sorted(audio_files)

def process_audio_batch(
    directory: str,
    recursive: bool = False,
    model_name: str = "small",
    language: str = None,
    task: str = "transcribe",
    formats: List[str] = ["txt"]
) -> Dict[str, Any]:
    """Process all audio files in a directory."""
    
    # Find all audio files
    audio_files = find_audio_files(directory, recursive)
    
    if not audio_files:
        print(f"No audio files found in {directory}")
        return {}
    
    print(f"Found {len(audio_files)} audio files to process")
    
    # Initialize the transcriber (load model once for all files)
    transcriber = WhisperTranscriber(model_name=model_name)
    
    results = {}
    total_duration = 0
    
    # Process each file with a progress bar
    for audio_path in tqdm(audio_files, desc="Processing files"):
        start_time = time.time()
        
        try:
            # Process audio file
            audio_array, temp_file = process_audio_file(audio_path)
            
            # Transcribe
            result = transcriber.transcribe(
                audio_array,
                language=language,
                task=task
            )
            
            # Clean up temp file
            cleanup_temp_file(temp_file)
            
            # Save transcription
            output_path = os.path.splitext(audio_path)[0]
            output_files = save_transcription(
                result,
                output_path,
                formats=formats
            )
            
            # Calculate duration
            duration = time.time() - start_time
            total_duration += duration
            
            # Store results
            results[audio_path] = {
                'output_files': output_files,
                'language': result.language,
                'duration': duration
            }
            
            # Print completion message for this file
            print(f"Completed: {os.path.basename(audio_path)} ({result.language}) in {duration:.2f}s")
            
        except Exception as e:
            print(f"Error processing {audio_path}: {str(e)}")
    
    # Print summary
    print(f"\nBatch processing complete!")
    print(f"Processed {len(results)}/{len(audio_files)} files successfully")
    print(f"Total processing time: {total_duration:.2f} seconds")
    
    return results

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Batch process audio files for transcription")
    parser.add_argument("directory", help="Directory containing audio files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process subdirectories")
    parser.add_argument("-m", "--model", default="small", help="Whisper model size")
    parser.add_argument("-l", "--language", default=None, help="Language code (None for auto)")
    parser.add_argument("-t", "--task", default="transcribe", choices=["transcribe", "translate"], 
                       help="Task to perform")
    parser.add_argument("-f", "--formats", default="txt", help="Output formats (comma-separated)")
    
    args = parser.parse_args()
    
    # Convert formats string to list
    formats = args.formats.split(",")
    
    # Process the batch
    process_audio_batch(
        directory=args.directory,
        recursive=args.recursive,
        model_name=args.model,
        language=args.language,
        task=args.task,
        formats=formats
    )
    
    return 0

if __name__ == "__main__":
    main() 