"""
Postprocessor module for offline-transcriber.
Handles the conversion of transcription results to various output formats.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, TextIO

from .transcriber import TranscriptionResult, Segment

logger = logging.getLogger(__name__)


def _format_timestamp(seconds: float, format_type: str = "srt") -> str:
    """
    Format time in seconds to SRT/WebVTT timestamp format.
    
    Args:
        seconds: Time in seconds
        format_type: "srt" or "vtt"
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    
    if format_type.lower() == "srt":
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    elif format_type.lower() == "vtt":
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    else:
        raise ValueError(f"Unsupported format type: {format_type}")


def generate_plain_text(result: TranscriptionResult) -> str:
    """
    Generate plain text output from transcription result.
    
    Args:
        result: TranscriptionResult object
        
    Returns:
        Plain text content
    """
    return result.text


def generate_srt(result: TranscriptionResult) -> str:
    """
    Generate SRT (SubRip) format from transcription result.
    
    Args:
        result: TranscriptionResult object
        
    Returns:
        SRT formatted content
    """
    srt_lines = []
    
    for segment in result.segments:
        # Segment number
        srt_lines.append(str(segment.id + 1))
        
        # Timestamps
        start_time = _format_timestamp(segment.start)
        end_time = _format_timestamp(segment.end)
        srt_lines.append(f"{start_time} --> {end_time}")
        
        # Text content
        srt_lines.append(segment.text)
        
        # Empty line between entries
        srt_lines.append("")
    
    return "\n".join(srt_lines)


def generate_vtt(result: TranscriptionResult) -> str:
    """
    Generate WebVTT format from transcription result.
    
    Args:
        result: TranscriptionResult object
        
    Returns:
        WebVTT formatted content
    """
    vtt_lines = ["WEBVTT", ""]
    
    for segment in result.segments:
        # Timestamp line
        start_time = _format_timestamp(segment.start, "vtt")
        end_time = _format_timestamp(segment.end, "vtt")
        vtt_lines.append(f"{start_time} --> {end_time}")
        
        # Text content
        vtt_lines.append(segment.text)
        
        # Empty line between entries
        vtt_lines.append("")
    
    return "\n".join(vtt_lines)


def generate_json(result: TranscriptionResult) -> str:
    """
    Generate JSON format from transcription result.
    
    Args:
        result: TranscriptionResult object
        
    Returns:
        JSON formatted content
    """
    json_dict = {
        "text": result.text,
        "language": result.language,
        "segments": [
            {
                "id": segment.id,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
            for segment in result.segments
        ]
    }
    
    return json.dumps(json_dict, ensure_ascii=False, indent=2)


def save_transcription(
    result: TranscriptionResult,
    output_path: str,
    formats: List[str] = ["txt"]
) -> Dict[str, str]:
    """
    Save transcription result in multiple formats.
    
    Args:
        result: TranscriptionResult object
        output_path: Base path for output files (without extension)
        formats: List of formats to save ("txt", "srt", "vtt", "json")
        
    Returns:
        Dictionary mapping format to file path
    """
    format_generators = {
        "txt": generate_plain_text,
        "srt": generate_srt,
        "vtt": generate_vtt,
        "json": generate_json
    }
    
    saved_files = {}
    
    for fmt in formats:
        if fmt.lower() not in format_generators:
            logger.warning(f"Unsupported output format: {fmt}")
            continue
        
        file_path = f"{output_path}.{fmt.lower()}"
        content = format_generators[fmt.lower()](result)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Saved {fmt.upper()} output to: {file_path}")
            saved_files[fmt.lower()] = file_path
            
        except Exception as e:
            logger.error(f"Failed to save {fmt.upper()} output: {e}")
    
    return saved_files 