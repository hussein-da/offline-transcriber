"""
Tests for the postprocessor module.
"""

import json
import os
import tempfile
from unittest import mock

import pytest

from offline_transcriber import postprocessor
from offline_transcriber.transcriber import Segment, TranscriptionResult


@pytest.fixture
def sample_result():
    """Create a sample transcription result for testing."""
    return TranscriptionResult(
        text="This is a test transcription with multiple segments.",
        segments=[
            Segment(id=0, start=0.0, end=2.5, text="This is a test"),
            Segment(id=1, start=2.5, end=5.0, text="transcription with"),
            Segment(id=2, start=5.0, end=7.5, text="multiple segments."),
        ],
        language="en"
    )


def test_format_timestamp():
    """Test SRT and VTT timestamp formatting."""
    # Test SRT format
    assert postprocessor._format_timestamp(3661.5) == "01:01:01,500"
    assert postprocessor._format_timestamp(0.001) == "00:00:00,001"
    assert postprocessor._format_timestamp(59.999) == "00:00:59,999"
    
    # Test VTT format
    assert postprocessor._format_timestamp(3661.5, "vtt") == "01:01:01.500"
    assert postprocessor._format_timestamp(0.001, "vtt") == "00:00:00.001"
    
    # Test invalid format
    with pytest.raises(ValueError):
        postprocessor._format_timestamp(1.0, "invalid")


def test_generate_plain_text(sample_result):
    """Test plain text generation."""
    text = postprocessor.generate_plain_text(sample_result)
    assert text == sample_result.text
    assert text == "This is a test transcription with multiple segments."


def test_generate_srt(sample_result):
    """Test SRT format generation."""
    srt = postprocessor.generate_srt(sample_result)
    
    # Check format
    lines = srt.strip().split("\n")
    
    # First segment
    assert lines[0] == "1"  # Segment number
    assert lines[1] == "00:00:00,000 --> 00:00:02,500"  # Timestamp
    assert lines[2] == "This is a test"  # Text
    
    # Second segment
    assert lines[4] == "2"
    assert lines[5] == "00:00:02,500 --> 00:00:05,000"
    assert lines[6] == "transcription with"
    
    # Third segment
    assert lines[8] == "3"
    assert lines[9] == "00:00:05,000 --> 00:00:07,500"
    assert lines[10] == "multiple segments."


def test_generate_vtt(sample_result):
    """Test WebVTT format generation."""
    vtt = postprocessor.generate_vtt(sample_result)
    
    # Check format
    lines = vtt.strip().split("\n")
    
    # Header
    assert lines[0] == "WEBVTT"
    
    # First segment
    assert lines[2] == "00:00:00.000 --> 00:00:02.500"
    assert lines[3] == "This is a test"
    
    # Second segment
    assert lines[5] == "00:00:02.500 --> 00:00:05.000"
    assert lines[6] == "transcription with"
    
    # Third segment
    assert lines[8] == "00:00:05.000 --> 00:00:07.500"
    assert lines[9] == "multiple segments."


def test_generate_json(sample_result):
    """Test JSON format generation."""
    json_str = postprocessor.generate_json(sample_result)
    
    # Parse the JSON
    data = json.loads(json_str)
    
    # Check contents
    assert data["text"] == "This is a test transcription with multiple segments."
    assert data["language"] == "en"
    assert len(data["segments"]) == 3
    
    # Check segments
    assert data["segments"][0]["id"] == 0
    assert data["segments"][0]["start"] == 0.0
    assert data["segments"][0]["end"] == 2.5
    assert data["segments"][0]["text"] == "This is a test"


def test_save_transcription(sample_result, tmp_path):
    """Test saving transcription in multiple formats."""
    output_path = os.path.join(tmp_path, "output")
    
    # Save in all formats
    formats = ["txt", "srt", "vtt", "json"]
    result = postprocessor.save_transcription(sample_result, output_path, formats)
    
    # Check returned paths
    assert set(result.keys()) == set(formats)
    assert all(os.path.exists(path) for path in result.values())
    
    # Check file contents
    with open(result["txt"], "r", encoding="utf-8") as f:
        assert f.read() == "This is a test transcription with multiple segments."
    
    with open(result["json"], "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["language"] == "en"
        assert len(data["segments"]) == 3


def test_save_transcription_invalid_format(sample_result, tmp_path):
    """Test saving with an invalid format."""
    output_path = os.path.join(tmp_path, "output")
    
    # Mock logger to check warning
    with mock.patch("offline_transcriber.postprocessor.logger") as mock_logger:
        result = postprocessor.save_transcription(sample_result, output_path, ["txt", "invalid"])
        
        # Check only valid format was saved
        assert list(result.keys()) == ["txt"]
        assert os.path.exists(result["txt"])
        
        # Check warning was logged
        mock_logger.warning.assert_called_with("Unsupported output format: invalid")


def test_save_transcription_file_error(sample_result, tmp_path):
    """Test error handling when saving fails."""
    output_path = os.path.join(tmp_path, "output")
    
    # Mock open to simulate file error
    with mock.patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with mock.patch("offline_transcriber.postprocessor.logger") as mock_logger:
            result = postprocessor.save_transcription(sample_result, output_path, ["txt"])
            
            # Check no files were saved
            assert result == {}
            
            # Check error was logged
            mock_logger.error.assert_called_with(mock.ANY) 