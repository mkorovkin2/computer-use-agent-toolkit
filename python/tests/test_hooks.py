"""
Tests for hook system.
"""

import pytest
from computer_use_agent.hooks import HookRegistry
from computer_use_agent.types import AgentContext


def test_hook_registry_init():
    """Test HookRegistry initialization."""
    registry = HookRegistry()
    assert len(registry.before_screenshot) == 0
    assert len(registry.after_action) == 0


def test_register_before_screenshot():
    """Test registering before_screenshot hook."""
    registry = HookRegistry()
    called = []
    
    @registry.register_before_screenshot
    def hook(context):
        called.append(True)
    
    context = AgentContext()
    registry.trigger_before_screenshot(context)
    
    assert len(called) == 1


def test_register_after_action():
    """Test registering after_action hook."""
    registry = HookRegistry()
    actions = []
    
    @registry.register_after_action
    def hook(context, action, result):
        actions.append(action)
    
    context = AgentContext()
    registry.trigger_after_action(context, {"type": "click"}, None)
    
    assert len(actions) == 1
    assert actions[0]["type"] == "click"


def test_register_on_tool_call():
    """Test registering tool call hook."""
    registry = HookRegistry()
    calls = []
    
    @registry.register_on_tool_call("click", None)
    def hook(context, args):
        calls.append(args)
    
    context = AgentContext()
    args = {"x": 100, "y": 200}
    result = registry.trigger_on_tool_call(context, "click", args)
    
    assert len(calls) == 1
    assert result == args


def test_tool_call_hook_modification():
    """Test that tool call hooks can modify args."""
    registry = HookRegistry()
    
    @registry.register_on_tool_call("click", None)
    def hook(context, args):
        # Modify args
        return {**args, "button": "right"}
    
    context = AgentContext()
    args = {"x": 100, "y": 200, "button": "left"}
    result = registry.trigger_on_tool_call(context, "click", args)
    
    assert result["button"] == "right"


def test_wildcard_tool_hook():
    """Test wildcard tool hook."""
    registry = HookRegistry()
    calls = []
    
    @registry.register_on_tool_call(None, None)
    def hook(context, tool_name, args):
        calls.append(tool_name)
    
    context = AgentContext()
    registry.trigger_on_tool_call(context, "click", {})
    registry.trigger_on_tool_call(context, "type", {})
    
    assert len(calls) == 2
    assert "click" in calls
    assert "type" in calls


def test_iteration_hooks():
    """Test iteration start/end hooks."""
    registry = HookRegistry()
    iterations = []
    
    @registry.register_on_iteration_start
    def start_hook(context, iteration):
        iterations.append(("start", iteration))
    
    @registry.register_on_iteration_end
    def end_hook(context, iteration):
        iterations.append(("end", iteration))
    
    context = AgentContext()
    registry.trigger_on_iteration_start(context, 0)
    registry.trigger_on_iteration_end(context, 0)
    
    assert len(iterations) == 2
    assert iterations[0] == ("start", 0)
    assert iterations[1] == ("end", 0)


def test_multiple_hooks():
    """Test multiple hooks of same type."""
    registry = HookRegistry()
    calls = []
    
    @registry.register_before_screenshot
    def hook1(context):
        calls.append(1)
    
    @registry.register_before_screenshot
    def hook2(context):
        calls.append(2)
    
    context = AgentContext()
    registry.trigger_before_screenshot(context)
    
    assert len(calls) == 2
    assert calls == [1, 2]

