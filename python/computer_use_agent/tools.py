"""
Tool definitions for Claude computer use.
"""

from typing import Any, Dict, List


def create_computer_tool_schema() -> Dict[str, Any]:
    """
    Create the Claude computer tool schema.
    This is the standard computer use tool that combines multiple actions.
    
    Returns:
        Tool schema dict.
    """
    return {
        "name": "computer",
        "type": "computer_20241022",
        "display_width_px": 1920,
        "display_height_px": 1080,
        "display_number": 1,
    }


def create_screenshot_tool() -> Dict[str, Any]:
    """Create screenshot tool schema."""
    return {
        "name": "screenshot",
        "description": "Take a screenshot of the current screen or a specific region",
        "input_schema": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "object",
                    "description": "Optional region to capture",
                    "properties": {
                        "x": {"type": "integer"},
                        "y": {"type": "integer"},
                        "width": {"type": "integer"},
                        "height": {"type": "integer"},
                    },
                },
            },
        },
    }


def create_mouse_move_tool() -> Dict[str, Any]:
    """Create mouse move tool schema."""
    return {
        "name": "mouse_move",
        "description": "Move the mouse cursor to specific coordinates",
        "input_schema": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "X coordinate to move to",
                },
                "y": {
                    "type": "integer",
                    "description": "Y coordinate to move to",
                },
                "duration": {
                    "type": "number",
                    "description": "Duration of movement in seconds",
                    "default": 0.5,
                },
            },
            "required": ["x", "y"],
        },
    }


def create_click_tool() -> Dict[str, Any]:
    """Create click tool schema."""
    return {
        "name": "click",
        "description": "Click at specific coordinates",
        "input_schema": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "X coordinate to click",
                },
                "y": {
                    "type": "integer",
                    "description": "Y coordinate to click",
                },
                "button": {
                    "type": "string",
                    "enum": ["left", "right", "middle"],
                    "description": "Mouse button to click",
                    "default": "left",
                },
                "clicks": {
                    "type": "integer",
                    "description": "Number of clicks",
                    "default": 1,
                },
            },
            "required": ["x", "y"],
        },
    }


def create_type_tool() -> Dict[str, Any]:
    """Create type tool schema."""
    return {
        "name": "type",
        "description": "Type text using the keyboard",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to type",
                },
                "interval": {
                    "type": "number",
                    "description": "Interval between keystrokes in seconds",
                    "default": 0.0,
                },
            },
            "required": ["text"],
        },
    }


def create_key_tool() -> Dict[str, Any]:
    """Create key press tool schema."""
    return {
        "name": "key",
        "description": "Press a keyboard key",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "Key to press (e.g., 'enter', 'tab', 'escape', 'backspace')",
                },
            },
            "required": ["key"],
        },
    }


def create_scroll_tool() -> Dict[str, Any]:
    """Create scroll tool schema."""
    return {
        "name": "scroll",
        "description": "Scroll in a direction",
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "left", "right"],
                    "description": "Direction to scroll",
                },
                "amount": {
                    "type": "integer",
                    "description": "Amount to scroll (number of clicks)",
                    "default": 3,
                },
                "x": {
                    "type": "integer",
                    "description": "Optional X coordinate to scroll at",
                },
                "y": {
                    "type": "integer",
                    "description": "Optional Y coordinate to scroll at",
                },
            },
            "required": ["direction"],
        },
    }


def get_default_tools() -> List[Dict[str, Any]]:
    """
    Get the default set of computer use tools.
    
    Returns:
        List of tool schemas.
    """
    return [
        create_screenshot_tool(),
        create_mouse_move_tool(),
        create_click_tool(),
        create_type_tool(),
        create_key_tool(),
        create_scroll_tool(),
    ]


def create_custom_tool_schema(
    name: str,
    description: str,
    input_schema: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create a custom tool schema.
    
    Args:
        name: Tool name.
        description: Tool description.
        input_schema: JSON schema for tool input.
        
    Returns:
        Tool schema dict.
    """
    return {
        "name": name,
        "description": description,
        "input_schema": input_schema,
    }


def generate_tool_schema_from_function(func) -> Dict[str, Any]:
    """
    Generate tool schema from a Python function using its signature and docstring.
    
    Args:
        func: Python function to generate schema for.
        
    Returns:
        Tool schema dict.
    """
    import inspect
    from typing import get_type_hints
    
    name = func.__name__
    description = func.__doc__ or f"Execute {name}"
    
    # Get function signature
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    properties = {}
    required = []
    
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        
        param_type = type_hints.get(param_name, Any)
        param_schema = _python_type_to_json_schema(param_type)
        
        properties[param_name] = param_schema
        
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    input_schema = {
        "type": "object",
        "properties": properties,
    }
    
    if required:
        input_schema["required"] = required
    
    return create_custom_tool_schema(name, description, input_schema)


def _python_type_to_json_schema(python_type) -> Dict[str, Any]:
    """Convert Python type hint to JSON schema."""
    type_mapping = {
        str: {"type": "string"},
        int: {"type": "integer"},
        float: {"type": "number"},
        bool: {"type": "boolean"},
        list: {"type": "array"},
        dict: {"type": "object"},
    }
    
    # Handle Optional types
    if hasattr(python_type, "__origin__"):
        origin = python_type.__origin__
        if origin is list:
            return {"type": "array"}
        elif origin is dict:
            return {"type": "object"}
    
    return type_mapping.get(python_type, {"type": "string"})

