"""
Main agent class that orchestrates the computer use agent loop.
"""

import time
import logging
from typing import Any, Callable, Dict, Iterator, List, Optional
from anthropic import Anthropic

from computer_use_agent.screen import ScreenCapture
from computer_use_agent.actions import ActionExecutor
from computer_use_agent.tools import get_default_tools
from computer_use_agent.workflow import WorkflowEngine
from computer_use_agent.hooks import HookRegistry
from computer_use_agent.types import (
    ActionResult,
    ActionType,
    AgentContext,
    AgentStep,
    MouseButton,
    ScreenRegion,
    ScrollDirection,
)

# Setup logger
logger = logging.getLogger(__name__)


class ComputerUseAgent:
    """
    Main agent class for building computer use agents with Claude.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        screen_region: Optional[ScreenRegion] = None,
        allowed_action_region: Optional[ScreenRegion] = None,
        safety_delay: float = 0.1,
        confirmation_mode: str = "auto",
        max_tokens: int = 4096,
        verbose: bool = True,
    ):
        """
        Initialize the computer use agent.
        
        Args:
            api_key: Anthropic API key.
            model: Claude model to use.
            screen_region: Optional region of screen to capture.
            allowed_action_region: Optional region where actions are allowed.
            safety_delay: Delay after each action.
            confirmation_mode: 'auto', 'confirm', or 'dry-run'.
            max_tokens: Maximum tokens for Claude responses.
            verbose: Enable verbose logging.
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.verbose = verbose
        
        # Initialize components
        self.client = Anthropic(api_key=api_key)
        self.screen = ScreenCapture(region=screen_region)
        self.executor = ActionExecutor(
            allowed_region=allowed_action_region,
            safety_delay=safety_delay,
            confirmation_mode=confirmation_mode,
        )
        self.workflow = WorkflowEngine()
        self.hooks = HookRegistry()
        
        # Agent state
        self.context = AgentContext()
        self.messages: List[Dict[str, Any]] = []
        
        # Get screen size for tool definition
        self.screen_width, self.screen_height = self.screen.get_screen_size()
        
        if self.verbose:
            logger.info(f"🤖 Agent initialized with model: {model}")
    
    @property
    def state(self) -> Dict[str, Any]:
        """Get agent state dict."""
        return self.context.state
    
    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        input_schema: Optional[Dict[str, Any]] = None,
    ):
        """
        Decorator to register a custom tool.
        
        Usage:
            @agent.tool(name="my_tool")
            def my_tool(arg1: str, arg2: int) -> dict:
                return {"result": "success"}
        """
        return self.workflow.register_tool(name, description, input_schema)
    
    def on_before_screenshot(self, func: Callable):
        """Decorator to register before_screenshot hook."""
        return self.hooks.register_before_screenshot(func)
    
    def on_after_screenshot(self, func: Callable):
        """Decorator to register after_screenshot hook."""
        return self.hooks.register_after_screenshot(func)
    
    def on_before_action(self, func: Callable):
        """Decorator to register before_action hook."""
        return self.hooks.register_before_action(func)
    
    def on_after_action(self, func: Callable):
        """Decorator to register after_action hook."""
        return self.hooks.register_after_action(func)
    
    def on_tool_call(self, tool_name: Optional[str] = None):
        """
        Decorator to register tool call hook.
        
        Args:
            tool_name: Specific tool name, or None for all tools.
        """
        def decorator(func: Callable):
            return self.hooks.register_on_tool_call(tool_name, func)
        return decorator
    
    def on_iteration_start(self, func: Callable):
        """Decorator to register iteration start hook."""
        return self.hooks.register_on_iteration_start(func)
    
    def on_iteration_end(self, func: Callable):
        """Decorator to register iteration end hook."""
        return self.hooks.register_on_iteration_end(func)
    
    def when(self, action_type: str, condition: Callable):
        """
        Decorator for conditional workflow handlers.
        
        Usage:
            @agent.when("click", lambda ctx, action: action.x > 500)
            def on_right_click(context, action):
                # Handle clicks on right side of screen
                pass
        """
        def decorator(func: Callable):
            self.workflow.register_conditional_handler(action_type, condition, func)
            return func
        return decorator
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a custom tool directly.
        
        Args:
            tool_name: Name of the tool.
            **kwargs: Tool arguments.
            
        Returns:
            Tool result.
        """
        return self.workflow.execute_tool(tool_name, **kwargs)
    
    def _build_tools(self) -> List[Dict[str, Any]]:
        """Build the full tool list including custom tools."""
        tools = get_default_tools()
        tools.extend(self.workflow.get_tool_schemas())
        return tools
    
    def _take_screenshot(self) -> str:
        """Take a screenshot and return as base64."""
        if self.verbose:
            logger.info("📸 Taking screenshot...")
        
        self.hooks.trigger_before_screenshot(self.context)
        
        image_b64 = self.screen.capture_base64()
        self.context.last_screenshot = image_b64
        
        self.hooks.trigger_after_screenshot(self.context, image_b64)
        
        if self.verbose:
            logger.info(f"✓ Screenshot captured ({len(image_b64)} bytes)")
        
        return image_b64
    
    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> ActionResult:
        """Execute a tool call from Claude."""
        # Trigger tool call hooks
        tool_input = self.hooks.trigger_on_tool_call(self.context, tool_name, tool_input)
        
        # Check if it's a custom tool
        if self.workflow.has_tool(tool_name):
            try:
                result = self.workflow.execute_tool(tool_name, **tool_input)
                return ActionResult(
                    success=True,
                    action_type=ActionType.SCREENSHOT,  # Placeholder
                    data={"result": result}
                )
            except Exception as e:
                return ActionResult(
                    success=False,
                    action_type=ActionType.SCREENSHOT,
                    error=str(e)
                )
        
        # Handle built-in tools
        if tool_name == "screenshot":
            image_b64 = self._take_screenshot()
            return ActionResult(
                success=True,
                action_type=ActionType.SCREENSHOT,
                data={"image": image_b64}
            )
        
        elif tool_name == "mouse_move":
            action = self.hooks.trigger_before_action(self.context, tool_input)
            result = self.executor.mouse_move(
                action["x"],
                action["y"],
                action.get("duration", 0.5)
            )
            self.hooks.trigger_after_action(self.context, tool_input, result)
            self.workflow.check_conditional_handlers(self.context, "mouse_move", tool_input)
            return result
        
        elif tool_name == "click":
            action = self.hooks.trigger_before_action(self.context, tool_input)
            result = self.executor.click(
                action["x"],
                action["y"],
                MouseButton(action.get("button", "left")),
                action.get("clicks", 1)
            )
            self.hooks.trigger_after_action(self.context, tool_input, result)
            self.workflow.check_conditional_handlers(self.context, "click", tool_input)
            return result
        
        elif tool_name == "type":
            action = self.hooks.trigger_before_action(self.context, tool_input)
            result = self.executor.type_text(
                action["text"],
                action.get("interval", 0.0)
            )
            self.hooks.trigger_after_action(self.context, tool_input, result)
            self.workflow.check_conditional_handlers(self.context, "type", tool_input)
            return result
        
        elif tool_name == "key":
            action = self.hooks.trigger_before_action(self.context, tool_input)
            result = self.executor.press_key(action["key"])
            self.hooks.trigger_after_action(self.context, tool_input, result)
            self.workflow.check_conditional_handlers(self.context, "key", tool_input)
            return result
        
        elif tool_name == "scroll":
            action = self.hooks.trigger_before_action(self.context, tool_input)
            result = self.executor.scroll(
                ScrollDirection(action["direction"]),
                action.get("amount", 3),
                action.get("x"),
                action.get("y")
            )
            self.hooks.trigger_after_action(self.context, tool_input, result)
            self.workflow.check_conditional_handlers(self.context, "scroll", tool_input)
            return result
        
        else:
            return ActionResult(
                success=False,
                action_type=ActionType.SCREENSHOT,
                error=f"Unknown tool: {tool_name}"
            )
    
    def run(
        self,
        goal: str,
        max_iterations: int = 20,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run the agent with a goal.
        
        Args:
            goal: The goal for the agent to achieve.
            max_iterations: Maximum number of iterations.
            system_prompt: Optional custom system prompt.
            
        Returns:
            Dict with results.
        """
        # Reset state
        self.context = AgentContext()
        self.messages = []
        
        # Initial screenshot
        initial_screenshot = self._take_screenshot()
        
        # Create initial message
        self.messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": initial_screenshot,
                    }
                },
                {
                    "type": "text",
                    "text": goal,
                }
            ]
        })
        
        system = system_prompt or (
            "You are a computer use agent. You can see the screen and take actions "
            "like clicking, typing, and scrolling. Analyze what you see and take "
            "appropriate actions to achieve the given goal."
        )
        
        for iteration in range(max_iterations):
            self.context.iteration = iteration
            
            if self.verbose:
                logger.info(f"\n{'='*60}")
                logger.info(f"🔄 Iteration {iteration + 1}/{max_iterations}")
                logger.info(f"{'='*60}")
            
            self.hooks.trigger_on_iteration_start(self.context, iteration)
            
            try:
                # Call Claude
                if self.verbose:
                    logger.info("🧠 Calling Claude API...")
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=system,
                    messages=self.messages,
                    tools=self._build_tools(),
                )
                
                # Add assistant response to messages
                self.messages.append({
                    "role": "assistant",
                    "content": response.content,
                })
                
                if self.verbose:
                    logger.info(f"✓ Claude responded (stop_reason: {response.stop_reason})")
                    # Log reasoning if present
                    for block in response.content:
                        if hasattr(block, "text") and block.text:
                            logger.info(f"💭 Reasoning: {block.text[:150]}...")
                            break
                
                # Check if done
                if response.stop_reason == "end_turn":
                    if self.verbose:
                        logger.info("✓ Agent completed successfully!")
                    self.hooks.trigger_on_iteration_end(self.context, iteration)
                    break
                
                # Execute tool calls
                if response.stop_reason == "tool_use":
                    tool_results = []
                    
                    for block in response.content:
                        if block.type == "tool_use":
                            if self.verbose:
                                logger.info(f"⚡ Executing tool: {block.name}")
                                logger.info(f"   Args: {block.input}")
                            
                            result = self._execute_tool(block.name, block.input)
                            self.context.action_history.append(result)
                            
                            if self.verbose:
                                status = "✓" if result.success else "✗"
                                logger.info(f"{status} Tool result: {result.success}")
                            
                            # Build tool result
                            tool_result_content = []
                            
                            if result.success:
                                if block.name == "screenshot" and result.data:
                                    tool_result_content.append({
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/png",
                                            "data": result.data["image"],
                                        }
                                    })
                                else:
                                    tool_result_content.append({
                                        "type": "text",
                                        "text": f"Success: {result.data}"
                                    })
                            else:
                                tool_result_content.append({
                                    "type": "text",
                                    "text": f"Error: {result.error}"
                                })
                            
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": tool_result_content,
                            })
                    
                    # Add tool results to messages
                    self.messages.append({
                        "role": "user",
                        "content": tool_results,
                    })
                
                self.hooks.trigger_on_iteration_end(self.context, iteration)
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "iteration": iteration,
                    "state": self.context.state,
                }
        
        return {
            "success": True,
            "iterations": self.context.iteration + 1,
            "state": self.context.state,
            "action_history": self.context.action_history,
        }
    
    def run_iter(
        self,
        goal: str,
        max_iterations: int = 20,
        system_prompt: Optional[str] = None,
    ) -> Iterator[AgentStep]:
        """
        Run the agent with step-by-step control.
        
        Yields:
            AgentStep for each iteration.
        """
        # Reset state
        self.context = AgentContext()
        self.messages = []
        
        # Initial screenshot
        initial_screenshot = self._take_screenshot()
        
        # Create initial message
        self.messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": initial_screenshot,
                    }
                },
                {
                    "type": "text",
                    "text": goal,
                }
            ]
        })
        
        system = system_prompt or (
            "You are a computer use agent. You can see the screen and take actions "
            "like clicking, typing, and scrolling. Analyze what you see and take "
            "appropriate actions to achieve the given goal."
        )
        
        for iteration in range(max_iterations):
            self.context.iteration = iteration
            self.hooks.trigger_on_iteration_start(self.context, iteration)
            
            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=self.messages,
                tools=self._build_tools(),
            )
            
            # Add assistant response
            self.messages.append({
                "role": "assistant",
                "content": response.content,
            })
            
            # Extract reasoning
            reasoning = None
            for block in response.content:
                if hasattr(block, "text"):
                    reasoning = block.text
                    break
            
            # Check if done
            if response.stop_reason == "end_turn":
                yield AgentStep(
                    iteration=iteration,
                    reasoning=reasoning,
                )
                self.hooks.trigger_on_iteration_end(self.context, iteration)
                break
            
            # Execute tool calls
            if response.stop_reason == "tool_use":
                tool_results = []
                
                for block in response.content:
                    if block.type == "tool_use":
                        result = self._execute_tool(block.name, block.input)
                        self.context.action_history.append(result)
                        
                        # Yield step
                        yield AgentStep(
                            iteration=iteration,
                            action=ActionType(block.name) if block.name in [e.value for e in ActionType] else None,
                            reasoning=reasoning,
                            result=result,
                        )
                        
                        # Build tool result
                        tool_result_content = []
                        
                        if result.success:
                            if block.name == "screenshot" and result.data:
                                tool_result_content.append({
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": result.data["image"],
                                    }
                                })
                            else:
                                tool_result_content.append({
                                    "type": "text",
                                    "text": f"Success: {result.data}"
                                })
                        else:
                            tool_result_content.append({
                                "type": "text",
                                "text": f"Error: {result.error}"
                            })
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result_content,
                        })
                
                # Add tool results
                self.messages.append({
                    "role": "user",
                    "content": tool_results,
                })
            
            self.hooks.trigger_on_iteration_end(self.context, iteration)
    
    def close(self):
        """Close agent resources."""
        self.screen.close()

