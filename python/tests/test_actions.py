"""
Tests for action executor module.
"""

import pytest
from computer_use_agent.actions import ActionExecutor
from computer_use_agent.types import ActionType, MouseButton, ScrollDirection, ScreenRegion


def test_action_executor_init():
    """Test ActionExecutor initialization."""
    executor = ActionExecutor()
    assert executor.allowed_region is None
    assert executor.safety_delay == 0.1
    assert executor.confirmation_mode == "auto"


def test_action_executor_dry_run():
    """Test dry-run mode."""
    executor = ActionExecutor(confirmation_mode="dry-run")
    result = executor.click(100, 100)
    assert result.success is True
    assert result.data["dry_run"] is True


def test_allowed_region_check():
    """Test allowed region checking."""
    region = ScreenRegion(x=100, y=100, width=200, height=200)
    executor = ActionExecutor(allowed_region=region)
    
    # Inside region
    assert executor._check_allowed(150, 150) is True
    
    # Outside region
    assert executor._check_allowed(50, 50) is False


def test_mouse_move_outside_allowed_region():
    """Test mouse move outside allowed region."""
    region = ScreenRegion(x=100, y=100, width=200, height=200)
    executor = ActionExecutor(allowed_region=region, confirmation_mode="dry-run")
    
    result = executor.mouse_move(50, 50)
    assert result.success is False
    assert "outside allowed region" in result.error


def test_click_action():
    """Test click action in dry-run mode."""
    executor = ActionExecutor(confirmation_mode="dry-run")
    result = executor.click(100, 100)
    assert result.success is True
    assert result.action_type == ActionType.CLICK


def test_double_click():
    """Test double click."""
    executor = ActionExecutor(confirmation_mode="dry-run")
    result = executor.double_click(100, 100)
    assert result.success is True


def test_type_text():
    """Test typing text."""
    executor = ActionExecutor(confirmation_mode="dry-run")
    result = executor.type_text("Hello, World!")
    assert result.success is True
    assert result.action_type == ActionType.TYPE


def test_press_key():
    """Test pressing a key."""
    executor = ActionExecutor(confirmation_mode="dry-run")
    result = executor.press_key("enter")
    assert result.success is True
    assert result.action_type == ActionType.KEY


def test_scroll():
    """Test scrolling."""
    executor = ActionExecutor(confirmation_mode="dry-run")
    result = executor.scroll(ScrollDirection.DOWN, amount=5)
    assert result.success is True
    assert result.action_type == ActionType.SCROLL


def test_get_mouse_position():
    """Test getting mouse position."""
    executor = ActionExecutor()
    x, y = executor.get_mouse_position()
    assert isinstance(x, int)
    assert isinstance(y, int)


def test_get_screen_size():
    """Test getting screen size."""
    executor = ActionExecutor()
    width, height = executor.get_screen_size()
    assert width > 0
    assert height > 0

