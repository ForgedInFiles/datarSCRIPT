"""Graphics builtins using PySide6."""

from typing import Any, List, Tuple
from .base import BuiltinRegistry
from ..errors import DatarError
from ..graphics.context import GraphicsContext


def _ensure_ctx() -> GraphicsContext:
    return GraphicsContext.get()


@BuiltinRegistry.register("graphics_init")
def graphics_init(
    title: str = "DatarScript", width: int = 800, height: int = 600
) -> None:
    ctx = _ensure_ctx()
    ctx.init(str(title), int(width), int(height))


@BuiltinRegistry.register("graphics_set_background")
def graphics_set_background(color: str) -> None:
    ctx = _ensure_ctx()
    ctx.set_background(color)


@BuiltinRegistry.register("graphics_set_color")
def graphics_set_color(color: str) -> None:
    """Set the current drawing color."""
    ctx = _ensure_ctx()
    ctx.set_color(color)


@BuiltinRegistry.register("graphics_draw_rect")
def graphics_draw_rect(
    x: float, y: float, w: float, h: float, color: str = "black"
) -> None:
    ctx = _ensure_ctx()
    ctx.draw_rect(x, y, w, h, color)


@BuiltinRegistry.register("graphics_draw_ellipse")
def graphics_draw_ellipse(
    x: float, y: float, w: float, h: float, color: str = "black"
) -> None:
    ctx = _ensure_ctx()
    ctx.draw_ellipse(x, y, w, h, color)


@BuiltinRegistry.register("graphics_draw_polygon")
def graphics_draw_polygon(
    points: List[Tuple[float, float]], color: str = "black"
) -> None:
    ctx = _ensure_ctx()
    ctx.draw_polygon(points, color)


@BuiltinRegistry.register("graphics_draw_line")
def graphics_draw_line(
    x1: float, y1: float, x2: float, y2: float, color: str = "black", width: int = 1
) -> None:
    ctx = _ensure_ctx()
    ctx.draw_line(x1, y1, x2, y2, color, int(width))


@BuiltinRegistry.register("graphics_draw_text")
def graphics_draw_text(
    text: str, x: float, y: float, size: int = 12, color: str = "white"
) -> None:
    ctx = _ensure_ctx()
    ctx.draw_text(x, y, text, color, int(size))


@BuiltinRegistry.register("graphics_load_image")
def graphics_load_image(path: str) -> str:
    ctx = _ensure_ctx()
    return ctx.load_image(path)


@BuiltinRegistry.register("graphics_draw_image")
def graphics_draw_image(
    handle: str, x: float, y: float, w: float | None = None, h: float | None = None
) -> None:
    ctx = _ensure_ctx()
    ctx.draw_image(handle, x, y, w, h)


@BuiltinRegistry.register("graphics_on")
def graphics_on(event_type: str, handler_name: str, interpreter: Any) -> None:
    """Register an event handler."""
    ctx = _ensure_ctx()
    ctx.on_event(event_type, handler_name, interpreter)


@BuiltinRegistry.register("graphics_show")
def graphics_show(blocking: bool = True) -> None:
    ctx = _ensure_ctx()
    ctx.show(blocking=blocking)


@BuiltinRegistry.register("graphics_process_events")
def graphics_process_events() -> str:
    """Process events and return the last key pressed."""
    ctx = _ensure_ctx()
    return ctx.process_events()


@BuiltinRegistry.register("graphics_clear")
def graphics_clear() -> None:
    ctx = _ensure_ctx()
    ctx.clear()


@BuiltinRegistry.register("rgb")
def rgb_color(r: int, g: int, b: int) -> str:
    """Create a color string from RGB values."""
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


# Removed random_int - there's already randint in math_stdlib


@BuiltinRegistry.register("length")
def length(lst: list) -> int:
    """Get the length of a list."""
    if not isinstance(lst, list):
        raise DatarError("length: argument must be a list")
    return len(lst)


@BuiltinRegistry.register("get_item")
def get_item(lst: list, index: int) -> Any:
    """Get an item from a list by index."""
    if not isinstance(lst, list):
        raise DatarError("get_item: first argument must be a list")
    return lst[int(index)]


@BuiltinRegistry.register("slice")
def slice_list(lst: list, start: int, end: int) -> list:
    """Get a slice of a list."""
    if not isinstance(lst, list):
        raise DatarError("slice: first argument must be a list")
    return lst[int(start) : int(end)]


@BuiltinRegistry.register("current_time_ms")
def current_time_ms() -> int:
    """Get current time in milliseconds."""
    import time

    return int(time.time() * 1000)
