"""
Tests for utility functions.
"""

import pytest
from PIL import Image
from computer_use_agent.utils import (
    scale_coordinates,
    normalize_coordinates,
    denormalize_coordinates,
    is_coordinate_in_region,
    calculate_region_center,
    expand_region,
    validate_coordinates,
    clamp_coordinates,
    PerformanceTimer,
)
from computer_use_agent.types import ScreenRegion


def test_scale_coordinates():
    """Test scaling coordinates."""
    x, y = scale_coordinates(100, 100, (1920, 1080), (3840, 2160))
    assert x == 200
    assert y == 200


def test_normalize_coordinates():
    """Test normalizing coordinates."""
    norm_x, norm_y = normalize_coordinates(960, 540, (1920, 1080))
    assert abs(norm_x - 0.5) < 0.01
    assert abs(norm_y - 0.5) < 0.01


def test_denormalize_coordinates():
    """Test denormalizing coordinates."""
    x, y = denormalize_coordinates(0.5, 0.5, (1920, 1080))
    assert x == 960
    assert y == 540


def test_is_coordinate_in_region():
    """Test checking if coordinate is in region."""
    region = ScreenRegion(x=100, y=100, width=200, height=200)
    
    assert is_coordinate_in_region(150, 150, region) is True
    assert is_coordinate_in_region(250, 250, region) is True
    assert is_coordinate_in_region(50, 50, region) is False
    assert is_coordinate_in_region(350, 350, region) is False


def test_calculate_region_center():
    """Test calculating region center."""
    region = ScreenRegion(x=100, y=100, width=200, height=200)
    center_x, center_y = calculate_region_center(region)
    assert center_x == 200
    assert center_y == 200


def test_expand_region():
    """Test expanding region."""
    region = ScreenRegion(x=100, y=100, width=200, height=200)
    expanded = expand_region(region, padding=10)
    assert expanded.x == 90
    assert expanded.y == 90
    assert expanded.width == 220
    assert expanded.height == 220


def test_expand_region_at_edge():
    """Test expanding region at screen edge."""
    region = ScreenRegion(x=0, y=0, width=100, height=100)
    expanded = expand_region(region, padding=10)
    assert expanded.x == 0  # Clamped to 0
    assert expanded.y == 0


def test_validate_coordinates():
    """Test coordinate validation."""
    assert validate_coordinates(100, 100, 1920, 1080) is True
    assert validate_coordinates(-10, 100, 1920, 1080) is False
    assert validate_coordinates(100, -10, 1920, 1080) is False
    assert validate_coordinates(2000, 100, 1920, 1080) is False


def test_clamp_coordinates():
    """Test clamping coordinates."""
    x, y = clamp_coordinates(-10, -10, 1920, 1080)
    assert x == 0
    assert y == 0
    
    x, y = clamp_coordinates(2000, 1100, 1920, 1080)
    assert x == 1919
    assert y == 1079


def test_performance_timer():
    """Test performance timer."""
    import time
    
    with PerformanceTimer("test") as timer:
        time.sleep(0.01)
    
    assert timer.elapsed_ms >= 10

