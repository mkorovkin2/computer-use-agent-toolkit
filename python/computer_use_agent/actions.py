"""
Action executor module for performing mouse and keyboard actions.
"""

import time
from typing import Optional, Tuple
import pyautogui

from computer_use_agent.types import (
    ActionResult,
    ActionType,
    MouseButton,
    ScrollDirection,
    ScreenRegion,
)


class ActionExecutor:
    """
    Executes computer actions like mouse movements, clicks, typing, and scrolling.
    """
    
    def __init__(
        self,
        allowed_region: Optional[ScreenRegion] = None,
        safety_delay: float = 0.1,
        confirmation_mode: str = "auto",
        rate_limit_delay: float = 0.05,
    ):
        """
        Initialize action executor.
        
        Args:
            allowed_region: Optional region where actions are allowed. If None, allows full screen.
            safety_delay: Delay in seconds after each action.
            confirmation_mode: 'auto', 'confirm', or 'dry-run'.
            rate_limit_delay: Minimum delay between actions.
        """
        self.allowed_region = allowed_region
        self.safety_delay = safety_delay
        self.confirmation_mode = confirmation_mode
        self.rate_limit_delay = rate_limit_delay
        self._last_action_time = 0.0
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = rate_limit_delay
    
    def _check_allowed(self, x: int, y: int) -> bool:
        """Check if coordinates are in allowed region."""
        if not self.allowed_region:
            return True
        
        return (
            self.allowed_region.x <= x <= self.allowed_region.x + self.allowed_region.width
            and self.allowed_region.y <= y <= self.allowed_region.y + self.allowed_region.height
        )
    
    def _rate_limit(self):
        """Enforce rate limiting between actions."""
        elapsed = time.time() - self._last_action_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self._last_action_time = time.time()
    
    def _execute_with_safety(self, action_func, action_type: ActionType):
        """Execute an action with safety checks."""
        if self.confirmation_mode == "dry-run":
            return ActionResult(
                success=True,
                action_type=action_type,
                data={"dry_run": True}
            )
        
        self._rate_limit()
        
        try:
            result = action_func()
            time.sleep(self.safety_delay)
            return ActionResult(
                success=True,
                action_type=action_type,
                data=result
            )
        except Exception as e:
            return ActionResult(
                success=False,
                action_type=action_type,
                error=str(e)
            )
    
    def mouse_move(self, x: int, y: int, duration: float = 0.5) -> ActionResult:
        """
        Move mouse to coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            duration: Duration of movement in seconds.
            
        Returns:
            ActionResult.
        """
        if not self._check_allowed(x, y):
            return ActionResult(
                success=False,
                action_type=ActionType.MOUSE_MOVE,
                error=f"Coordinates ({x}, {y}) outside allowed region"
            )
        
        def move():
            pyautogui.moveTo(x, y, duration=duration)
            return {"x": x, "y": y}
        
        return self._execute_with_safety(move, ActionType.MOUSE_MOVE)
    
    def click(
        self, 
        x: int, 
        y: int, 
        button: MouseButton = MouseButton.LEFT,
        clicks: int = 1,
    ) -> ActionResult:
        """
        Click at coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            button: Mouse button to click.
            clicks: Number of clicks.
            
        Returns:
            ActionResult.
        """
        if not self._check_allowed(x, y):
            return ActionResult(
                success=False,
                action_type=ActionType.CLICK,
                error=f"Coordinates ({x}, {y}) outside allowed region"
            )
        
        def do_click():
            pyautogui.click(x, y, clicks=clicks, button=button.value)
            return {"x": x, "y": y, "button": button.value, "clicks": clicks}
        
        return self._execute_with_safety(do_click, ActionType.CLICK)
    
    def double_click(self, x: int, y: int) -> ActionResult:
        """
        Double click at coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            
        Returns:
            ActionResult.
        """
        return self.click(x, y, clicks=2)
    
    def type_text(self, text: str, interval: float = 0.0) -> ActionResult:
        """
        Type text.
        
        Args:
            text: Text to type.
            interval: Interval between keystrokes in seconds.
            
        Returns:
            ActionResult.
        """
        def do_type():
            pyautogui.write(text, interval=interval)
            return {"text": text, "length": len(text)}
        
        return self._execute_with_safety(do_type, ActionType.TYPE)
    
    def press_key(self, key: str) -> ActionResult:
        """
        Press a keyboard key.
        
        Args:
            key: Key name (e.g., 'enter', 'tab', 'escape').
            
        Returns:
            ActionResult.
        """
        def do_press():
            pyautogui.press(key)
            return {"key": key}
        
        return self._execute_with_safety(do_press, ActionType.KEY)
    
    def scroll(
        self, 
        direction: ScrollDirection, 
        amount: int = 3,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> ActionResult:
        """
        Scroll in a direction.
        
        Args:
            direction: Scroll direction.
            amount: Amount to scroll (clicks).
            x: Optional X coordinate to scroll at.
            y: Optional Y coordinate to scroll at.
            
        Returns:
            ActionResult.
        """
        if x is not None and y is not None:
            if not self._check_allowed(x, y):
                return ActionResult(
                    success=False,
                    action_type=ActionType.SCROLL,
                    error=f"Coordinates ({x}, {y}) outside allowed region"
                )
        
        def do_scroll():
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
            
            if direction == ScrollDirection.UP:
                pyautogui.scroll(amount)
            elif direction == ScrollDirection.DOWN:
                pyautogui.scroll(-amount)
            elif direction == ScrollDirection.LEFT:
                pyautogui.hscroll(-amount)
            elif direction == ScrollDirection.RIGHT:
                pyautogui.hscroll(amount)
            
            return {"direction": direction.value, "amount": amount}
        
        return self._execute_with_safety(do_scroll, ActionType.SCROLL)
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.
        
        Returns:
            Tuple of (x, y).
        """
        return pyautogui.position()
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get screen size.
        
        Returns:
            Tuple of (width, height).
        """
        return pyautogui.size()

