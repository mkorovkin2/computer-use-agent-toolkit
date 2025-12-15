"""
Utility functions for computer use agents.
"""

import logging
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from computer_use_agent.types import ScreenRegion


# Logging setup
def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """
    Setup logging for the agent.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_file: Optional file to log to.
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


# Coordinate utilities
def scale_coordinates(
    x: int,
    y: int,
    from_resolution: Tuple[int, int],
    to_resolution: Tuple[int, int],
) -> Tuple[int, int]:
    """
    Scale coordinates from one resolution to another.
    
    Args:
        x: X coordinate.
        y: Y coordinate.
        from_resolution: Source resolution (width, height).
        to_resolution: Target resolution (width, height).
        
    Returns:
        Scaled (x, y) coordinates.
    """
    from_width, from_height = from_resolution
    to_width, to_height = to_resolution
    
    scale_x = to_width / from_width
    scale_y = to_height / from_height
    
    return int(x * scale_x), int(y * scale_y)


def normalize_coordinates(
    x: int,
    y: int,
    resolution: Tuple[int, int],
) -> Tuple[float, float]:
    """
    Normalize coordinates to 0-1 range.
    
    Args:
        x: X coordinate.
        y: Y coordinate.
        resolution: Screen resolution (width, height).
        
    Returns:
        Normalized (x, y) coordinates in range [0, 1].
    """
    width, height = resolution
    return x / width, y / height


def denormalize_coordinates(
    norm_x: float,
    norm_y: float,
    resolution: Tuple[int, int],
) -> Tuple[int, int]:
    """
    Denormalize coordinates from 0-1 range to pixel coordinates.
    
    Args:
        norm_x: Normalized X coordinate.
        norm_y: Normalized Y coordinate.
        resolution: Screen resolution (width, height).
        
    Returns:
        Pixel (x, y) coordinates.
    """
    width, height = resolution
    return int(norm_x * width), int(norm_y * height)


def is_coordinate_in_region(
    x: int,
    y: int,
    region: ScreenRegion,
) -> bool:
    """
    Check if a coordinate is inside a region.
    
    Args:
        x: X coordinate.
        y: Y coordinate.
        region: Screen region.
        
    Returns:
        True if coordinate is in region.
    """
    return (
        region.x <= x <= region.x + region.width
        and region.y <= y <= region.y + region.height
    )


def calculate_region_center(region: ScreenRegion) -> Tuple[int, int]:
    """
    Calculate the center point of a region.
    
    Args:
        region: Screen region.
        
    Returns:
        Center (x, y) coordinates.
    """
    center_x = region.x + region.width // 2
    center_y = region.y + region.height // 2
    return center_x, center_y


def expand_region(
    region: ScreenRegion,
    padding: int,
) -> ScreenRegion:
    """
    Expand a region by adding padding.
    
    Args:
        region: Screen region.
        padding: Padding to add on all sides.
        
    Returns:
        Expanded region.
    """
    return ScreenRegion(
        x=max(0, region.x - padding),
        y=max(0, region.y - padding),
        width=region.width + 2 * padding,
        height=region.height + 2 * padding,
    )


# Screenshot annotation utilities
def annotate_screenshot(
    image: Image.Image,
    boxes: list[Tuple[int, int, int, int]],
    labels: Optional[list[str]] = None,
    box_color: str = "red",
    text_color: str = "white",
    box_width: int = 3,
) -> Image.Image:
    """
    Annotate a screenshot with boxes and labels.
    
    Args:
        image: PIL Image to annotate.
        boxes: List of (x, y, width, height) boxes.
        labels: Optional list of labels for each box.
        box_color: Color for boxes.
        text_color: Color for text.
        box_width: Width of box lines.
        
    Returns:
        Annotated image.
    """
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    
    try:
        font = ImageFont.truetype("Arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    for i, (x, y, w, h) in enumerate(boxes):
        # Draw box
        draw.rectangle(
            [(x, y), (x + w, y + h)],
            outline=box_color,
            width=box_width,
        )
        
        # Draw label
        if labels and i < len(labels):
            label = labels[i]
            # Draw background for text
            bbox = draw.textbbox((x, y - 20), label, font=font)
            draw.rectangle(bbox, fill=box_color)
            draw.text((x, y - 20), label, fill=text_color, font=font)
    
    return annotated


def draw_click_indicator(
    image: Image.Image,
    x: int,
    y: int,
    radius: int = 10,
    color: str = "red",
) -> Image.Image:
    """
    Draw a click indicator on an image.
    
    Args:
        image: PIL Image.
        x: X coordinate.
        y: Y coordinate.
        radius: Radius of indicator.
        color: Color of indicator.
        
    Returns:
        Image with indicator.
    """
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    
    # Draw circle
    draw.ellipse(
        [(x - radius, y - radius), (x + radius, y + radius)],
        outline=color,
        width=3,
    )
    
    # Draw crosshair
    draw.line([(x - radius - 5, y), (x + radius + 5, y)], fill=color, width=2)
    draw.line([(x, y - radius - 5), (x, y + radius + 5)], fill=color, width=2)
    
    return annotated


def create_grid_overlay(
    image: Image.Image,
    grid_size: int = 100,
    color: str = "blue",
    opacity: int = 50,
) -> Image.Image:
    """
    Create a grid overlay on an image for debugging.
    
    Args:
        image: PIL Image.
        grid_size: Size of grid cells in pixels.
        color: Grid line color.
        opacity: Opacity of grid lines (0-255).
        
    Returns:
        Image with grid overlay.
    """
    from PIL import Image as PILImage
    
    overlay = PILImage.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    width, height = image.size
    
    # Draw vertical lines
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=color + str(hex(opacity)[2:]), width=1)
    
    # Draw horizontal lines
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=color + str(hex(opacity)[2:]), width=1)
    
    # Composite
    image_rgba = image.convert("RGBA")
    return PILImage.alpha_composite(image_rgba, overlay).convert("RGB")


# Validation utilities
def validate_coordinates(
    x: int,
    y: int,
    screen_width: int,
    screen_height: int,
) -> bool:
    """
    Validate that coordinates are within screen bounds.
    
    Args:
        x: X coordinate.
        y: Y coordinate.
        screen_width: Screen width.
        screen_height: Screen height.
        
    Returns:
        True if valid.
    """
    return 0 <= x < screen_width and 0 <= y < screen_height


def clamp_coordinates(
    x: int,
    y: int,
    screen_width: int,
    screen_height: int,
) -> Tuple[int, int]:
    """
    Clamp coordinates to screen bounds.
    
    Args:
        x: X coordinate.
        y: Y coordinate.
        screen_width: Screen width.
        screen_height: Screen height.
        
    Returns:
        Clamped (x, y) coordinates.
    """
    clamped_x = max(0, min(x, screen_width - 1))
    clamped_y = max(0, min(y, screen_height - 1))
    return clamped_x, clamped_y


# Performance utilities
class PerformanceTimer:
    """Simple performance timer for profiling."""
    
    def __init__(self, name: str = "Timer"):
        """Initialize timer."""
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """Start timer."""
        import time
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timer and log."""
        import time
        self.end_time = time.time()
        elapsed = (self.end_time - self.start_time) * 1000
        logger = get_logger(__name__)
        logger.debug(f"{self.name}: {elapsed:.2f}ms")
    
    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

