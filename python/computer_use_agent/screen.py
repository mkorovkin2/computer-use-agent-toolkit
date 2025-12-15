"""
Screen capture module for taking screenshots.
"""

import base64
import io
from typing import Optional, Tuple
from PIL import Image
import mss

from computer_use_agent.types import ScreenRegion


class ScreenCapture:
    """
    Handles screen capture with support for full screen, windows, and custom regions.
    """
    
    def __init__(
        self,
        region: Optional[ScreenRegion] = None,
        monitor: int = 1,
    ):
        """
        Initialize screen capture.
        
        Args:
            region: Optional screen region to capture. If None, captures full screen.
            monitor: Monitor number to capture from (1-indexed).
        """
        self.region = region
        self.monitor = monitor
        self._sct = mss.mss()
    
    def capture(self, region: Optional[ScreenRegion] = None) -> Image.Image:
        """
        Capture a screenshot.
        
        Args:
            region: Optional region to capture. Overrides instance region if provided.
            
        Returns:
            PIL Image object.
        """
        capture_region = region or self.region
        
        if capture_region:
            # Capture specific region
            monitor_info = {
                "left": capture_region.x,
                "top": capture_region.y,
                "width": capture_region.width,
                "height": capture_region.height,
            }
        else:
            # Capture full monitor
            monitor_info = self._sct.monitors[self.monitor]
        
        screenshot = self._sct.grab(monitor_info)
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    
    def capture_base64(
        self, 
        region: Optional[ScreenRegion] = None,
        format: str = "PNG",
    ) -> str:
        """
        Capture a screenshot and return as base64 string (for Claude API).
        
        Args:
            region: Optional region to capture.
            format: Image format (PNG, JPEG).
            
        Returns:
            Base64 encoded image string.
        """
        image = self.capture(region)
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")
    
    def capture_with_metadata(
        self, 
        region: Optional[ScreenRegion] = None,
    ) -> Tuple[Image.Image, dict]:
        """
        Capture a screenshot with metadata.
        
        Args:
            region: Optional region to capture.
            
        Returns:
            Tuple of (image, metadata dict).
        """
        image = self.capture(region)
        metadata = {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "region": region,
            "monitor": self.monitor,
        }
        return image, metadata
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the size of the current monitor.
        
        Returns:
            Tuple of (width, height).
        """
        monitor = self._sct.monitors[self.monitor]
        return monitor["width"], monitor["height"]
    
    def get_monitor_count(self) -> int:
        """
        Get the number of available monitors.
        
        Returns:
            Number of monitors.
        """
        return len(self._sct.monitors) - 1  # First monitor is "all monitors"
    
    def close(self):
        """Close the screen capture resources."""
        self._sct.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

