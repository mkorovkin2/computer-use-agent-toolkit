"""
Workflow engine for custom tools and conditional logic.
"""

from typing import Any, Callable, Dict, List, Optional
from computer_use_agent.tools import generate_tool_schema_from_function, create_custom_tool_schema
from computer_use_agent.types import ToolDefinition


class WorkflowEngine:
    """
    Manages custom tools and workflow logic.
    """
    
    def __init__(self):
        """Initialize workflow engine."""
        self.custom_tools: Dict[str, ToolDefinition] = {}
        self.conditional_handlers: Dict[str, List[tuple]] = {}
    
    def register_tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        input_schema: Optional[Dict[str, Any]] = None,
    ):
        """
        Decorator to register a custom tool.
        
        Args:
            name: Tool name (defaults to function name).
            description: Tool description (defaults to docstring).
            input_schema: JSON schema for tool input (auto-generated if not provided).
        """
        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            
            if input_schema:
                schema = create_custom_tool_schema(
                    tool_name,
                    description or func.__doc__ or f"Execute {tool_name}",
                    input_schema
                )
            else:
                schema = generate_tool_schema_from_function(func)
                if description:
                    schema["description"] = description
            
            self.custom_tools[tool_name] = ToolDefinition(
                name=tool_name,
                description=schema["description"],
                input_schema=schema["input_schema"],
                function=func
            )
            
            return func
        
        return decorator
    
    def register_conditional_handler(
        self,
        action_type: str,
        condition: Callable,
        handler: Callable,
    ):
        """
        Register a conditional handler for an action type.
        
        Args:
            action_type: Type of action to handle.
            condition: Condition function that returns True/False.
            handler: Handler function to execute when condition is met.
        """
        if action_type not in self.conditional_handlers:
            self.conditional_handlers[action_type] = []
        self.conditional_handlers[action_type].append((condition, handler))
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a custom tool.
        
        Args:
            tool_name: Name of the tool to execute.
            **kwargs: Tool arguments.
            
        Returns:
            Tool result.
        """
        if tool_name not in self.custom_tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.custom_tools[tool_name]
        return tool.function(**kwargs)
    
    def check_conditional_handlers(self, context, action_type: str, action):
        """
        Check and execute conditional handlers for an action.
        
        Args:
            context: Agent context.
            action_type: Type of action.
            action: Action data.
        """
        if action_type not in self.conditional_handlers:
            return
        
        for condition, handler in self.conditional_handlers[action_type]:
            try:
                if condition(context, action):
                    handler(context, action)
            except Exception as e:
                print(f"Error in conditional handler: {e}")
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Get all custom tool schemas.
        
        Returns:
            List of tool schemas.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self.custom_tools.values()
        ]
    
    def has_tool(self, tool_name: str) -> bool:
        """
        Check if a tool is registered.
        
        Args:
            tool_name: Tool name.
            
        Returns:
            True if tool exists.
        """
        return tool_name in self.custom_tools

