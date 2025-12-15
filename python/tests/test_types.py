"""
Tests for type definitions.
"""

import pytest
from computer_use_agent.types import (
    ActionResult,
    ActionType,
    AgentContext,
    ScreenRegion,
    MouseButton,
    ScrollDirection,
)


def test_screen_region():
    """Test ScreenRegion creation."""
    region = ScreenRegion(x=10, y=20, width=100, height=200)
    assert region.x == 10
    assert region.y == 20
    assert region.width == 100
    assert region.height == 200


def test_action_result():
    """Test ActionResult creation."""
    result = ActionResult(
        success=True,
        action_type=ActionType.CLICK,
        data={"x": 100, "y": 200}
    )
    assert result.success is True
    assert result.action_type == ActionType.CLICK
    assert result.data["x"] == 100


def test_action_result_failure():
    """Test ActionResult with error."""
    result = ActionResult(
        success=False,
        action_type=ActionType.TYPE,
        error="Failed to type text"
    )
    assert result.success is False
    assert result.error == "Failed to type text"


def test_agent_context():
    """Test AgentContext initialization."""
    context = AgentContext()
    assert context.state == {}
    assert context.iteration == 0
    assert context.action_history == []
    assert context.last_screenshot is None


def test_agent_context_state():
    """Test AgentContext state management."""
    context = AgentContext()
    context.state["key"] = "value"
    assert context.state["key"] == "value"


def test_enums():
    """Test enum values."""
    assert ActionType.CLICK.value == "click"
    assert MouseButton.LEFT.value == "left"
    assert ScrollDirection.UP.value == "up"

