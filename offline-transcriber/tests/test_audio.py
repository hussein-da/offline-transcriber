"""
Tests for the audio processing module.
"""

import os
import tempfile
from unittest import mock

import numpy as np
import pytest
from pydub import AudioSegment

from offline_transcriber import audio


def create_test_audio():
    """Create a simple test audio segment."""
    # Create a simple sine wave
    sample_rate = 16000
    duration_sec = 1
    frequency = 440  # Hz (A4 note)
    
    # Generate sine wave
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    
    # Convert to int16 for audio
    audio_data = (sine_wave * 32767).astype(np.int16)
    
    # Create AudioSegment
    return AudioSegment(
        audio_data.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,  # 16-bit audio
        channels=1
    )


def test_load_audio(tmp_path):
    """Test loading an audio file."""
    # Create a temporary WAV file
    temp_audio = create_test_audio()
    temp_file = os.path.join(tmp_path, "test_audio.wav")
    temp_audio.export(temp_file, format="wav")
    
    # Test loading
    loaded_audio = audio.load_audio(temp_file)
    
    # Basic validation
    assert isinstance(loaded_audio, AudioSegment)
    assert abs(loaded_audio.duration_seconds - 1.0) < 0.1
    assert loaded_audio.frame_rate == 16000


def test_load_audio_not_found():
    """Test loading a non-existent file."""
    with pytest.raises(FileNotFoundError):
        audio.load_audio("nonexistent_file.wav")


def test_preprocess_audio():
    """Test audio preprocessing."""
    # Create stereo audio
    mono_audio = create_test_audio()
    stereo_audio = AudioSegment.from_mono_audiosegments(mono_audio, mono_audio)
    
    # Test stereo to mono conversion
    assert stereo_audio.channels == 2
    processed = audio.preprocess_audio(stereo_audio)
    assert processed.channels == 1
    
    # Test resampling
    high_rate_audio = mono_audio.set_frame_rate(44100)
    processed = audio.preprocess_audio(high_rate_audio)
    assert processed.frame_rate == 16000


def test_get_audio_array():
    """Test conversion to numpy array."""
    test_audio = create_test_audio()
    array = audio.get_audio_array(test_audio)
    
    # Check shape and type
    assert isinstance(array, np.ndarray)
    assert array.dtype == np.float32
    assert len(array) == test_audio.frame_count()
    
    # Check normalization (-1 to 1)
    assert -1.0 <= array.min() <= 0
    assert 0 <= array.max() <= 1.0


def test_save_temp_audio():
    """Test saving to temporary file."""
    test_audio = create_test_audio()
    temp_path = audio.save_temp_audio(test_audio)
    
    try:
        # Check file exists and is a wav
        assert os.path.exists(temp_path)
        assert temp_path.endswith(".wav")
        
        # Check content
        loaded = AudioSegment.from_file(temp_path)
        assert abs(loaded.duration_seconds - test_audio.duration_seconds) < 0.1
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_process_audio_file():
    """Test the complete audio processing pipeline."""
    # Create a temporary WAV file
    test_audio = create_test_audio()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        test_audio.export(temp_path, format="wav")
        
        # Process the file
        result_array, temp_wav = audio.process_audio_file(temp_path)
        
        # Check results
        assert isinstance(result_array, np.ndarray)
        assert os.path.exists(temp_wav)
        assert temp_wav.endswith(".wav")
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        audio.cleanup_temp_file(temp_wav)


def test_cleanup_temp_file():
    """Test temporary file cleanup."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
    
    # Verify it exists
    assert os.path.exists(temp_path)
    
    # Clean it up
    audio.cleanup_temp_file(temp_path)
    
    # Verify it's gone
    assert not os.path.exists(temp_path)
    
    # Test with None and non-existent file (should not raise)
    audio.cleanup_temp_file(None)
    audio.cleanup_temp_file("nonexistent_file.wav") 