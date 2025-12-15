"""
Hook system for workflow customization.
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class HookRegistry:
    """Registry for managing workflow hooks."""
    
    before_screenshot: List[Callable] = field(default_factory=list)
    after_screenshot: List[Callable] = field(default_factory=list)
    before_action: List[Callable] = field(default_factory=list)
    after_action: List[Callable] = field(default_factory=list)
    on_tool_call: Dict[str, List[Callable]] = field(default_factory=dict)
    on_iteration_start: List[Callable] = field(default_factory=list)
    on_iteration_end: List[Callable] = field(default_factory=list)
    
    def register_before_screenshot(self, func: Callable):
        """Register a hook to run before taking a screenshot."""
        self.before_screenshot.append(func)
        return func
    
    def register_after_screenshot(self, func: Callable):
        """Register a hook to run after taking a screenshot."""
        self.after_screenshot.append(func)
        return func
    
    def register_before_action(self, func: Callable):
        """Register a hook to run before executing an action."""
        self.before_action.append(func)
        return func
    
    def register_after_action(self, func: Callable):
        """Register a hook to run after executing an action."""
        self.after_action.append(func)
        return func
    
    def register_on_tool_call(self, tool_name: Optional[str], func: Callable):
        """
        Register a hook to run when a tool is called.
        
        Args:
            tool_name: Specific tool name, or None for all tools.
            func: Hook function.
        """
        key = tool_name or "*"
        if key not in self.on_tool_call:
            self.on_tool_call[key] = []
        self.on_tool_call[key].append(func)
        return func
    
    def register_on_iteration_start(self, func: Callable):
        """Register a hook to run at the start of each iteration."""
        self.on_iteration_start.append(func)
        return func
    
    def register_on_iteration_end(self, func: Callable):
        """Register a hook to run at the end of each iteration."""
        self.on_iteration_end.append(func)
        return func
    
    def trigger_before_screenshot(self, context):
        """Trigger all before_screenshot hooks."""
        for hook in self.before_screenshot:
            hook(context)
    
    def trigger_after_screenshot(self, context, image):
        """Trigger all after_screenshot hooks."""
        for hook in self.after_screenshot:
            hook(context, image)
    
    def trigger_before_action(self, context, action):
        """Trigger all before_action hooks."""
        for hook in self.before_action:
            result = hook(context, action)
            if result is not None:
                action = result
        return action
    
    def trigger_after_action(self, context, action, result):
        """Trigger all after_action hooks."""
        for hook in self.after_action:
            hook(context, action, result)
    
    def trigger_on_tool_call(self, context, tool_name: str, args: Dict[str, Any]):
        """Trigger tool call hooks."""
        # Trigger specific tool hooks
        if tool_name in self.on_tool_call:
            for hook in self.on_tool_call[tool_name]:
                result = hook(context, args)
                if result is not None:
                    args = result
        
        # Trigger wildcard hooks
        if "*" in self.on_tool_call:
            for hook in self.on_tool_call["*"]:
                result = hook(context, tool_name, args)
                if result is not None:
                    args = result
        
        return args
    
    def trigger_on_iteration_start(self, context, iteration: int):
        """Trigger iteration start hooks."""
        for hook in self.on_iteration_start:
            hook(context, iteration)
    
    def trigger_on_iteration_end(self, context, iteration: int):
        """Trigger iteration end hooks."""
        for hook in self.on_iteration_end:
            hook(context, iteration)

