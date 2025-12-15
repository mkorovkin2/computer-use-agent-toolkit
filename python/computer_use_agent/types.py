"""
Type definitions for the Computer Use Agent SDK.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum


class ActionType(str, Enum):
    """Types of actions the agent can perform."""
    SCREENSHOT = "screenshot"
    MOUSE_MOVE = "mouse_move"
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    TYPE = "type"
    KEY = "key"
    SCROLL = "scroll"


class ScrollDirection(str, Enum):
    """Scroll directions."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class MouseButton(str, Enum):
    """Mouse button types."""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


@dataclass
class ScreenRegion:
    """Defines a region of the screen to capture."""
    x: int
    y: int
    width: int
    height: int


@dataclass
class ActionResult:
    """Result of an action execution."""
    success: bool
    action_type: ActionType
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@dataclass
class AgentStep:
    """Represents a single step in the agent loop."""
    iteration: int
    action: Optional[ActionType] = None
    reasoning: Optional[str] = None
    result: Optional[ActionResult] = None
    waiting_for_confirmation: bool = False


@dataclass
class AgentContext:
    """Context passed to workflow hooks."""
    state: Dict[str, Any]
    iteration: int
    action_history: List[ActionResult]
    last_screenshot: Optional[bytes] = None
    last_screenshot_text: Optional[str] = None
    
    def __init__(self):
        self.state = {}
        self.iteration = 0
        self.action_history = []
        self.last_screenshot = None
        self.last_screenshot_text = None


@dataclass
class ToolDefinition:
    """Definition of a custom tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    function: Callable


# Type aliases for hooks
HookFunction = Callable[[AgentContext, Any], Any]
ToolFunction = Callable[..., Any]

