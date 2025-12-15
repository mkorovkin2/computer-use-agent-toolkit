"""
Tests for screen capture module.
"""

import pytest
from PIL import Image
from computer_use_agent.screen import ScreenCapture
from computer_use_agent.types import ScreenRegion


def test_screen_capture_init():
    """Test ScreenCapture initialization."""
    screen = ScreenCapture()
    assert screen.region is None
    assert screen.monitor == 1


def test_screen_capture_with_region():
    """Test ScreenCapture with custom region."""
    region = ScreenRegion(x=0, y=0, width=800, height=600)
    screen = ScreenCapture(region=region)
    assert screen.region == region


def test_capture():
    """Test capturing a screenshot."""
    with ScreenCapture() as screen:
        image = screen.capture()
        assert isinstance(image, Image.Image)
        assert image.width > 0
        assert image.height > 0


def test_capture_base64():
    """Test capturing screenshot as base64."""
    with ScreenCapture() as screen:
        b64_data = screen.capture_base64()
        assert isinstance(b64_data, str)
        assert len(b64_data) > 0


def test_capture_with_metadata():
    """Test capturing screenshot with metadata."""
    with ScreenCapture() as screen:
        image, metadata = screen.capture_with_metadata()
        assert isinstance(image, Image.Image)
        assert "width" in metadata
        assert "height" in metadata
        assert metadata["width"] == image.width
        assert metadata["height"] == image.height


def test_get_screen_size():
    """Test getting screen size."""
    with ScreenCapture() as screen:
        width, height = screen.get_screen_size()
        assert width > 0
        assert height > 0


def test_get_monitor_count():
    """Test getting monitor count."""
    with ScreenCapture() as screen:
        count = screen.get_monitor_count()
        assert count >= 1


def test_context_manager():
    """Test ScreenCapture context manager."""
    screen = ScreenCapture()
    with screen:
        assert screen._sct is not None
    # After context exit, resources should be cleaned up

