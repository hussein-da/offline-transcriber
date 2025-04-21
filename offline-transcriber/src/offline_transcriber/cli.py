"""
Command-line interface for offline-transcriber.
"""

import os
import sys
import glob
import time
import logging
import argparse
from typing import List, Optional, Dict, Any
from pathlib import Path

from tqdm import tqdm

from . import __version__
from .audio import process_audio_file, cleanup_temp_file
from .transcriber import WhisperTranscriber, TranscriptionResult, WHISPER_MODELS
from .postprocessor import save_transcription

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def setup_argparser() -> argparse.ArgumentParser:
    """Set up the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="transcribe",
        description="Offline-transcriber: A tool for transcribing audio files locally without an internet connection.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument(
        "input",
        help="Input audio file or directory",
        type=str,
    )
    
    parser.add_argument(
        "-m", "--model",
        help="Whisper model size to use",
        choices=WHISPER_MODELS,
        default="small",
        type=str,
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (without extension)",
        type=str,
    )
    
    parser.add_argument(
        "-f", "--formats",
        help="Output formats (comma-separated)",
        default="txt",
        type=str,
    )
    
    parser.add_argument(
        "-l", "--language",
        help="Language code (e.g., 'en', 'de', 'auto' for auto-detection)",
        default="auto",
        type=str,
    )
    
    parser.add_argument(
        "-t", "--task",
        help="Task to perform: transcribe or translate to English",
        choices=["transcribe", "translate"],
        default="transcribe",
        type=str,
    )
    
    parser.add_argument(
        "-b", "--batch",
        help="Process all audio files in the input directory",
        action="store_true",
    )
    
    parser.add_argument(
        "-r", "--recursive",
        help="Recursively process subdirectories (only with --batch)",
        action="store_true",
    )
    
    parser.add_argument(
        "-d", "--device",
        help="Device to use (cpu, cuda, cuda:0, etc.)",
        default=None,
        type=str,
    )
    
    parser.add_argument(
        "-v", "--verbose",
        help="Increase output verbosity",
        action="store_true",
    )
    
    parser.add_argument(
        "--version",
        help="Show version and exit",
        action="version",
        version=f"offline-transcriber v{__version__}",
    )
    
    return parser


def find_audio_files(input_path: str, recursive: bool = False) -> List[str]:
    """
    Find all audio files in a directory.
    
    Args:
        input_path: Path to directory
        recursive: Whether to search recursively
        
    Returns:
        List of audio file paths
    """
    # Audio file extensions to look for
    extensions = ["*.wav", "*.mp3", "*.flac", "*.aac", "*.ogg", "*.m4a"]
    
    audio_files = []
    
    if recursive:
        for ext in extensions:
            pattern = os.path.join(input_path, "**", ext)
            audio_files.extend(glob.glob(pattern, recursive=True))
    else:
        for ext in extensions:
            pattern = os.path.join(input_path, ext)
            audio_files.extend(glob.glob(pattern))
    
    return sorted(audio_files)


def get_output_path(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Determine the output file path.
    
    Args:
        input_path: Input audio file path
        output_path: User-specified output path
        
    Returns:
        Output path without extension
    """
    if output_path:
        # Strip any extension from user-provided output path
        return os.path.splitext(output_path)[0]
    
    # Use input path with extension stripped
    return os.path.splitext(input_path)[0]


def process_single_file(
    input_path: str,
    output_path: Optional[str] = None,
    model_name: str = "small",
    language: str = "auto",
    task: str = "transcribe",
    formats: List[str] = ["txt"],
    device: Optional[str] = None,
) -> Dict[str, str]:
    """
    Process a single audio file.
    
    Args:
        input_path: Input audio file path
        output_path: Output file path (without extension)
        model_name: Whisper model size
        language: Language code or "auto"
        task: "transcribe" or "translate"
        formats: List of output formats
        device: Device to use for transcription
        
    Returns:
        Dictionary mapping format to output file path
    """
    logger.info(f"Processing file: {input_path}")
    
    # Process audio file
    audio_array, temp_file = process_audio_file(input_path)
    
    try:
        # Initialize transcriber
        transcriber = WhisperTranscriber(model_name=model_name, device=device)
        
        # Set language to None if auto-detection is requested
        lang_param = None if language == "auto" else language
        
        # Transcribe audio
        result = transcriber.transcribe(
            audio_array,
            language=lang_param,
            task=task,
        )
        
        # Determine output path
        final_output_path = get_output_path(input_path, output_path)
        
        # Save transcription in requested formats
        return save_transcription(result, final_output_path, formats)
        
    finally:
        # Clean up temporary file
        cleanup_temp_file(temp_file)


def main() -> int:
    """Main entry point for the CLI."""
    parser = setup_argparser()
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Convert formats string to list
    formats = [fmt.strip() for fmt in args.formats.split(",")]
    
    # Process input
    start_time = time.time()
    
    try:
        if os.path.isfile(args.input):
            # Process single file
            output_files = process_single_file(
                input_path=args.input,
                output_path=args.output,
                model_name=args.model,
                language=args.language,
                task=args.task,
                formats=formats,
                device=args.device,
            )
            
            logger.info(f"Transcription saved to: {', '.join(output_files.values())}")
            
        elif os.path.isdir(args.input) and args.batch:
            # Process directory
            audio_files = find_audio_files(args.input, args.recursive)
            
            if not audio_files:
                logger.error(f"No audio files found in: {args.input}")
                return 1
            
            logger.info(f"Found {len(audio_files)} audio files to process")
            
            for audio_file in tqdm(audio_files, desc="Processing files"):
                try:
                    process_single_file(
                        input_path=audio_file,
                        output_path=None,  # Use input filename
                        model_name=args.model,
                        language=args.language,
                        task=args.task,
                        formats=formats,
                        device=args.device,
                    )
                except Exception as e:
                    logger.error(f"Failed to process {audio_file}: {e}")
            
            logger.info(f"Batch processing completed")
            
        else:
            if os.path.isdir(args.input) and not args.batch:
                logger.error(f"Input is a directory but --batch flag not set")
            else:
                logger.error(f"Input not found: {args.input}")
            return 1
        
        elapsed_time = time.time() - start_time
        logger.info(f"Total processing time: {elapsed_time:.2f} seconds")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            logger.exception("Detailed traceback:")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 