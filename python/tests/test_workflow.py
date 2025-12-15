"""
Tests for workflow engine.
"""

import pytest
from computer_use_agent.workflow import WorkflowEngine
from computer_use_agent.types import AgentContext


def test_workflow_engine_init():
    """Test WorkflowEngine initialization."""
    engine = WorkflowEngine()
    assert len(engine.custom_tools) == 0
    assert len(engine.conditional_handlers) == 0


def test_register_tool():
    """Test registering a custom tool."""
    engine = WorkflowEngine()
    
    @engine.register_tool(name="test_tool")
    def test_tool(arg: str) -> dict:
        """Test tool"""
        return {"result": arg}
    
    assert "test_tool" in engine.custom_tools
    assert engine.has_tool("test_tool")


def test_execute_tool():
    """Test executing a custom tool."""
    engine = WorkflowEngine()
    
    @engine.register_tool(name="add")
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b
    
    result = engine.execute_tool("add", a=5, b=3)
    assert result == 8


def test_execute_nonexistent_tool():
    """Test executing a tool that doesn't exist."""
    engine = WorkflowEngine()
    
    with pytest.raises(ValueError, match="not found"):
        engine.execute_tool("nonexistent")


def test_register_conditional_handler():
    """Test registering conditional handler."""
    engine = WorkflowEngine()
    called = []
    
    def condition(ctx, action):
        return action["x"] > 100
    
    def handler(ctx, action):
        called.append(True)
    
    engine.register_conditional_handler("click", condition, handler)
    
    # Test condition true
    context = AgentContext()
    engine.check_conditional_handlers(context, "click", {"x": 150, "y": 100})
    assert len(called) == 1
    
    # Test condition false
    engine.check_conditional_handlers(context, "click", {"x": 50, "y": 100})
    assert len(called) == 1  # Should not increment


def test_get_tool_schemas():
    """Test getting tool schemas."""
    engine = WorkflowEngine()
    
    @engine.register_tool(name="tool1")
    def tool1(arg: str) -> dict:
        """Tool 1"""
        return {}
    
    @engine.register_tool(name="tool2")
    def tool2(arg: int) -> dict:
        """Tool 2"""
        return {}
    
    schemas = engine.get_tool_schemas()
    assert len(schemas) == 2
    names = [s["name"] for s in schemas]
    assert "tool1" in names
    assert "tool2" in names

