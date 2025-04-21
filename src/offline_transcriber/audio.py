"""
Audio preprocessing module for offline-transcriber.
Handles loading, resampling, and conversion of audio files.
"""

import os
import tempfile
import logging
from typing import Optional, Tuple

import numpy as np
from pydub import AudioSegment

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000  # 16 kHz (required for most speech recognition models)


def load_audio(file_path: str) -> AudioSegment:
    """
    Load an audio file using pydub.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        AudioSegment object
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    # Handle different path formats
    file_path = os.path.abspath(os.path.expanduser(file_path))
    
    if not os.path.exists(file_path):
        # Try to look in the 'audio' directory if it exists
        audio_dir = os.path.join(os.getcwd(), 'audio')
        alternative_path = os.path.join(audio_dir, os.path.basename(file_path))
        
        if os.path.exists(alternative_path):
            file_path = alternative_path
            logger.info(f"Found audio file in audio directory: {file_path}")
        else:
            logger.error(f"Audio file not found: {file_path}")
            logger.error(f"Alternative path also not found: {alternative_path}")
            raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    try:
        # pydub can automatically detect the format from the file extension
        audio = AudioSegment.from_file(file_path)
        logger.info(f"Loaded audio file: {file_path} ({audio.duration_seconds:.2f} seconds)")
        return audio
    except Exception as e:
        logger.error(f"Failed to load audio file {file_path}: {e}")
        logger.error("Make sure FFmpeg is installed and in your PATH")
        logger.error("Download FFmpeg from: https://ffmpeg.org/download.html")
        raise ValueError(f"Failed to load audio file: {e}")


def preprocess_audio(audio: AudioSegment) -> AudioSegment:
    """
    Preprocess audio by converting to mono and resampling to 16kHz.
    
    Args:
        audio: AudioSegment to preprocess
        
    Returns:
        Preprocessed AudioSegment
    """
    # Convert to mono by averaging channels
    if audio.channels > 1:
        logger.debug(f"Converting from {audio.channels} channels to mono")
        audio = audio.set_channels(1)
    
    # Resample to 16kHz
    if audio.frame_rate != SAMPLE_RATE:
        logger.debug(f"Resampling from {audio.frame_rate}Hz to {SAMPLE_RATE}Hz")
        audio = audio.set_frame_rate(SAMPLE_RATE)
    
    return audio


def save_temp_audio(audio: AudioSegment) -> str:
    """
    Save audio to a temporary WAV file for processing.
    
    Args:
        audio: AudioSegment to save
        
    Returns:
        Path to the temporary WAV file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file.close()
    
    audio.export(temp_file.name, format="wav")
    logger.debug(f"Saved temporary audio file: {temp_file.name}")
    
    return temp_file.name


def get_audio_array(audio: AudioSegment) -> np.ndarray:
    """
    Convert AudioSegment to numpy array for processing with ML models.
    
    Args:
        audio: AudioSegment to convert
        
    Returns:
        Numpy array of audio samples (float32, normalized between -1 and 1)
    """
    # Get raw audio data
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    
    # Normalize to [-1.0, 1.0]
    max_possible_amplitude = 1 << (8 * audio.sample_width - 1)
    samples = samples / max_possible_amplitude
    
    return samples


def process_audio_file(file_path: str) -> Tuple[np.ndarray, str]:
    """
    Process an audio file: load, preprocess, and convert to numpy array.
    Also saves a temporary WAV file for models that require file input.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Tuple of (numpy array of processed audio, path to temp WAV file)
    """
    audio = load_audio(file_path)
    processed_audio = preprocess_audio(audio)
    
    # Save processed audio to temporary file
    temp_wav_path = save_temp_audio(processed_audio)
    
    # Convert to numpy array
    audio_array = get_audio_array(processed_audio)
    
    return audio_array, temp_wav_path


def cleanup_temp_file(temp_file_path: Optional[str]) -> None:
    """
    Clean up a temporary file if it exists.
    
    Args:
        temp_file_path: Path to the temporary file
    """
    if temp_file_path and os.path.exists(temp_file_path):
        try:
            os.unlink(temp_file_path)
            logger.debug(f"Removed temporary file: {temp_file_path}")
        except Exception as e:
            logger.warning(f"Failed to remove temporary file {temp_file_path}: {e}") 