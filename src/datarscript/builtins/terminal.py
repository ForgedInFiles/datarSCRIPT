"""Terminal/ANSI builtins for DatarScript - colors, cursor control, animations."""

import sys
import os
import time
from .base import BuiltinRegistry
from ..errors import DatarError


# ANSI color codes
COLORS = {
    "reset": "\u001b[0m",
    "bold": "\u001b[1m",
    "dim": "\u001b[2m",
    "italic": "\u001b[3m",
    "underline": "\u001b[4m",
    "blink": "\u001b[5m",
    "reverse": "\u001b[7m",
    "hidden": "\u001b[8m",
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "bg_black": "\u001b[40m",
    "bg_red": "\u001b[41m",
    "bg_green": "\u001b[42m",
    "bg_yellow": "\u001b[43m",
    "bg_blue": "\u001b[44m",
    "bg_magenta": "\u001b[45m",
    "bg_cyan": "\u001b[46m",
    "bg_white": "\u001b[47m",
}


@BuiltinRegistry.register("ansi_color")
def ansi_color(color: str) -> str:
    """Get ANSI color code by name."""
    if not isinstance(color, str):
        raise DatarError("ansi_color: color must be a string")
    return COLORS.get(color.lower(), "")


@BuiltinRegistry.register("ansi_reset")
def ansi_reset() -> str:
    """Reset all ANSI formatting."""
    return "\u001b[0m"


@BuiltinRegistry.register("cursor_hide")
def cursor_hide() -> str:
    """Hide cursor."""
    return "\u001b[?25l"


@BuiltinRegistry.register("cursor_show")
def cursor_show() -> str:
    """Show cursor."""
    return "\u001b[?25h"


@BuiltinRegistry.register("cursor_up")
def cursor_up(lines: int = 1) -> str:
    """Move cursor up N lines."""
    if not isinstance(lines, int):
        raise DatarError("cursor_up: lines must be an integer")
    return f"\u001b[{lines}A"


@BuiltinRegistry.register("cursor_down")
def cursor_down(lines: int = 1) -> str:
    """Move cursor down N lines."""
    if not isinstance(lines, int):
        raise DatarError("cursor_down: lines must be an integer")
    return f"\u001b[{lines}B"


@BuiltinRegistry.register("cursor_right")
def cursor_right(cols: int = 1) -> str:
    """Move cursor right N columns."""
    if not isinstance(cols, int):
        raise DatarError("cursor_right: cols must be an integer")
    return f"\u001b[{cols}C"


@BuiltinRegistry.register("cursor_left")
def cursor_left(cols: int = 1) -> str:
    """Move cursor left N columns."""
    if not isinstance(cols, int):
        raise DatarError("cursor_left: cols must be an integer")
    return f"\u001b[{cols}D"


@BuiltinRegistry.register("cursor_goto")
def cursor_goto(row: int, col: int) -> str:
    """Move cursor to specific row and column (1-based)."""
    if not isinstance(row, int) or not isinstance(col, int):
        raise DatarError("cursor_goto: row and col must be integers")
    return f"\u001b[{row};{col}H"


@BuiltinRegistry.register("clear_screen")
def clear_screen() -> str:
    """Clear the entire screen."""
    return "\u001b[2J\u001b[H"


@BuiltinRegistry.register("clear_line")
def clear_line() -> str:
    """Clear current line."""
    return "\u001b[2K"


@BuiltinRegistry.register("clear_to_end")
def clear_to_end() -> str:
    """Clear from cursor to end of line."""
    return "\u001b[K"


@BuiltinRegistry.register("print_raw")
def print_raw(text: str) -> None:
    """Print text without adding newline."""
    if not isinstance(text, str):
        raise DatarError("print_raw: text must be a string")
    print(text, end="", flush=True)


@BuiltinRegistry.register("flush_output")
def flush_output() -> None:
    """Flush stdout."""
    sys.stdout.flush()


@BuiltinRegistry.register("sleep_ms")
def sleep_ms(ms: int) -> None:
    """Sleep for specified milliseconds."""
    if not isinstance(ms, (int, float)):
        raise DatarError("sleep_ms: ms must be a number")
    time.sleep(ms / 1000.0)


@BuiltinRegistry.register("get_terminal_size")
def get_terminal_size() -> dict:
    """Get terminal size as {width, height}."""
    try:
        size = os.get_terminal_size()
        return {"width": size.columns, "height": size.lines}
    except Exception:
        return {"width": 80, "height": 24}


@BuiltinRegistry.register("is_tty")
def is_tty() -> bool:
    """Check if stdout is a TTY."""
    return sys.stdout.isatty()


# Spinner frames
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
DOTS_FRAMES = [".", "..", "..."]
BAR_FRAMES = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█", "▉", "▊", "▋", "▌", "▍", "▎"]


@BuiltinRegistry.register("spinner_frames")
def spinner_frames() -> list:
    """Get spinner animation frames."""
    return SPINNER_FRAMES


@BuiltinRegistry.register("dots_frames")
def dots_frames() -> list:
    """Get dots animation frames."""
    return DOTS_FRAMES


@BuiltinRegistry.register("bar_frames")
def bar_frames() -> list:
    """Get progress bar frames."""
    return BAR_FRAMES


@BuiltinRegistry.register("loading_animation")
def loading_animation(frame: int, style: str = "spinner") -> str:
    """Get loading animation frame."""
    if not isinstance(frame, int):
        raise DatarError("loading_animation: frame must be an integer")

    if style == "dots":
        frames = DOTS_FRAMES
    elif style == "bar":
        frames = BAR_FRAMES
    else:
        frames = SPINNER_FRAMES

    return frames[frame % len(frames)]


@BuiltinRegistry.register("colorize")
def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    if not isinstance(text, str) or not isinstance(color, str):
        raise DatarError("colorize: text and color must be strings")
    color_code = COLORS.get(color.lower(), "")
    if color_code:
        return color_code + text + "\u001b[0m"
    return text


@BuiltinRegistry.register("style_text")
def style_text(text: str, styles: list) -> str:
    """Apply multiple styles to text."""
    if not isinstance(text, str) or not isinstance(styles, list):
        raise DatarError("style_text: text must be string, styles must be list")

    result = text
    for style in reversed(styles):
        style_code = COLORS.get(str(style).lower(), "")
        if style_code:
            result = style_code + result
    return result + "\u001b[0m"
