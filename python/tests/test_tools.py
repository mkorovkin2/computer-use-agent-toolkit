"""
Tests for tool definitions.
"""

import pytest
from computer_use_agent.tools import (
    create_computer_tool_schema,
    create_screenshot_tool,
    create_click_tool,
    get_default_tools,
    create_custom_tool_schema,
    generate_tool_schema_from_function,
)


def test_create_computer_tool_schema():
    """Test creating computer tool schema."""
    schema = create_computer_tool_schema()
    assert schema["name"] == "computer"
    assert schema["type"] == "computer_20241022"


def test_create_screenshot_tool():
    """Test creating screenshot tool."""
    tool = create_screenshot_tool()
    assert tool["name"] == "screenshot"
    assert "description" in tool
    assert "input_schema" in tool


def test_create_click_tool():
    """Test creating click tool."""
    tool = create_click_tool()
    assert tool["name"] == "click"
    assert "x" in tool["input_schema"]["properties"]
    assert "y" in tool["input_schema"]["properties"]
    assert "x" in tool["input_schema"]["required"]
    assert "y" in tool["input_schema"]["required"]


def test_get_default_tools():
    """Test getting default tools."""
    tools = get_default_tools()
    assert len(tools) == 6
    tool_names = [tool["name"] for tool in tools]
    assert "screenshot" in tool_names
    assert "click" in tool_names
    assert "type" in tool_names


def test_create_custom_tool_schema():
    """Test creating custom tool schema."""
    schema = create_custom_tool_schema(
        name="my_tool",
        description="My custom tool",
        input_schema={
            "type": "object",
            "properties": {
                "arg": {"type": "string"}
            }
        }
    )
    assert schema["name"] == "my_tool"
    assert schema["description"] == "My custom tool"


def test_generate_tool_schema_from_function():
    """Test generating tool schema from function."""
    def my_function(name: str, age: int) -> dict:
        """A test function"""
        return {"name": name, "age": age}
    
    schema = generate_tool_schema_from_function(my_function)
    assert schema["name"] == "my_function"
    assert "name" in schema["input_schema"]["properties"]
    assert "age" in schema["input_schema"]["properties"]
    assert set(schema["input_schema"]["required"]) == {"name", "age"}


def test_generate_tool_schema_with_optional():
    """Test generating tool schema with optional parameters."""
    def my_function(required: str, optional: int = 42) -> dict:
        """A test function"""
        return {}
    
    schema = generate_tool_schema_from_function(my_function)
    assert "required" in schema["input_schema"]["required"]
    assert "optional" not in schema["input_schema"]["required"]

