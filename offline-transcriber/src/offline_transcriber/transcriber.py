"""
Transcriber module for offline-transcriber.
Handles transcription of audio files using OpenAI's Whisper model.
"""

import os
import logging
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass

# Import Whisper with error handling
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

logger = logging.getLogger(__name__)

# Available Whisper model sizes
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]


@dataclass
class Segment:
    """Class to represent a transcription segment with timing information."""
    id: int
    start: float  # Start time in seconds
    end: float    # End time in seconds
    text: str     # Transcribed text


@dataclass
class TranscriptionResult:
    """Class to represent complete transcription result."""
    text: str                 # Complete transcribed text
    segments: List[Segment]   # List of segments with timing
    language: str             # Detected language code


class WhisperTranscriber:
    """Transcriber using OpenAI's Whisper model."""
    
    def __init__(self, model_name: str = "small", device: Optional[str] = None):
        """
        Initialize the WhisperTranscriber.
        
        Args:
            model_name: Size of Whisper model to use ("tiny", "base", "small", "medium", "large")
            device: Device to run the model on (None for auto-detection, "cpu", or "cuda" for GPU)
        
        Raises:
            ImportError: If whisper is not installed
            ValueError: If the model_name is not valid
        """
        if not WHISPER_AVAILABLE:
            raise ImportError(
                "Whisper is not installed. Install it with: pip install openai-whisper"
            )
        
        if model_name not in WHISPER_MODELS:
            raise ValueError(
                f"Invalid model name: {model_name}. Choose from: {', '.join(WHISPER_MODELS)}"
            )
        
        self.model_name = model_name
        self.device = device
        self.model = None
        logger.info(f"Initializing WhisperTranscriber with model: {model_name}")
    
    def load_model(self) -> None:
        """
        Load the Whisper model if not already loaded.
        
        This is separated from __init__ to allow deferring the potentially
        large model loading until actually needed.
        """
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info(f"Whisper model loaded successfully")
    
    def _convert_whisper_segments(self, segments: List[Dict[str, Any]]) -> List[Segment]:
        """
        Convert Whisper's segment format to our Segment dataclass.
        
        Args:
            segments: List of segments from Whisper's transcribe output
            
        Returns:
            List of Segment objects
        """
        return [
            Segment(
                id=i,
                start=segment["start"],
                end=segment["end"],
                text=segment["text"].strip()
            )
            for i, segment in enumerate(segments)
        ]
    
    def transcribe(
        self,
        audio: Union[str, np.ndarray],
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> TranscriptionResult:
        """
        Transcribe audio to text.
        
        Args:
            audio: Either a path to an audio file or a numpy array of audio samples
            language: Language code (e.g., "en", "de", "ja") or None for auto-detection
            task: Either "transcribe" or "translate" (translate to English)
            
        Returns:
            TranscriptionResult with full text, segments, and detected language
            
        Raises:
            ValueError: If task is invalid or transcription fails
        """
        if task not in ["transcribe", "translate"]:
            raise ValueError(f"Invalid task: {task}. Choose from: transcribe, translate")
        
        # Load model if not already loaded
        self.load_model()
        
        try:
            logger.info(f"Starting transcription with task: {task}, language: {language or 'auto'}")
            
            # Run transcription
            result = self.model.transcribe(
                audio,
                language=language,
                task=task,
                verbose=False,
            )
            
            # Extract segments and full text
            segments = self._convert_whisper_segments(result["segments"])
            full_text = result["text"].strip()
            detected_language = result["language"]
            
            logger.info(f"Transcription completed. Detected language: {detected_language}")
            logger.debug(f"Transcribed {len(segments)} segments, {len(full_text)} characters")
            
            return TranscriptionResult(
                text=full_text,
                segments=segments,
                language=detected_language
            )
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise ValueError(f"Transcription failed: {e}")
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        Get a dictionary of language codes and names supported by Whisper.
        
        Returns:
            Dictionary mapping language codes to language names
        """
        self.load_model()
        tokenizer = self.model.tokenizer
        
        # Extract languages from tokenizer
        languages = {}
        for token, token_id in tokenizer.token_to_id.items():
            if token.startswith("<|") and token.endswith("|>") and not token.startswith("<|startoftranscript"):
                lang_code = token[2:-2]
                if lang_code not in ["translate", "transcribe", "notimestamps"]:
                    languages[lang_code] = tokenizer.decode([token_id]).strip()
        
        return languages 