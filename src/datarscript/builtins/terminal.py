"""Terminal/ANSI builtins for DatarScript - colors, cursor control, animations."""

import sys
import os
import time
import termios
import atexit
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

# Normalize terminal-specific escape sequences to canonical forms so key
# constants match across terminals (xterm, rxvt, application mode, etc.).
_ESCAPE_NORMALIZATION = {
    "\u001bOH": "\u001b[H",   # Home (application mode)
    "\u001bOF": "\u001b[F",   # End (application mode)
    "\u001b[1~": "\u001b[H",  # Home (rxvt)
    "\u001b[4~": "\u001b[F",  # End (rxvt)
    "\u001b[11~": "\u001bOP",  # F1 (rxvt)
    "\u001b[12~": "\u001bOQ",  # F2 (rxvt)
    "\u001b[13~": "\u001bOR",  # F3 (rxvt)
    "\u001b[14~": "\u001bOS",  # F4 (rxvt)
}

# Normalize single-byte control keys for consistency across terminals.
_SINGLE_KEY_NORMALIZATION = {
    "\u0008": "\u007f",  # Ctrl-H → DEL, so Backspace is consistent
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
    """Hide cursor (side effect)."""
    global _CURSOR_HIDDEN
    _CURSOR_HIDDEN = True
    sys.stdout.write("\u001b[?25l")
    sys.stdout.flush()
    return ""


@BuiltinRegistry.register("cursor_show")
def cursor_show() -> str:
    """Show cursor (side effect)."""
    global _CURSOR_HIDDEN
    _CURSOR_HIDDEN = False
    sys.stdout.write("\u001b[?25h")
    sys.stdout.flush()
    return ""


@BuiltinRegistry.register("cursorhome")
def cursorhome() -> str:
    """Move cursor to the home position (1,1)."""
    sys.stdout.write("\u001b[H")
    sys.stdout.flush()
    return ""


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
    """Clear the entire screen and return cursor to home position (1, 1)."""
    return "\u001b[2J\u001b[H"


@BuiltinRegistry.register("clearscreen")
def clearscreen() -> None:
    """
    Clear the screen for DatarScript:
    - Move cursor to home
    - Clear full viewport and scrollback so nothing remains
    """
    sys.stdout.write("\u001b[2J\u001b[3J\u001b[H")
    sys.stdout.flush()


@BuiltinRegistry.register("startscreen")
def startscreen() -> None:
    """Enter alternate screen, disable echo, hide cursor, clear once."""
    global _ALT_SCREEN, _CURSOR_HIDDEN, _TTY_SAVED
    if sys.stdin.isatty():
        if _TTY_SAVED is None:
            _TTY_SAVED = termios.tcgetattr(sys.stdin.fileno())
            new = termios.tcgetattr(sys.stdin.fileno())
            new[3] &= ~(termios.ECHO | termios.ICANON)
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, new)
    if not _ALT_SCREEN:
        sys.stdout.write("\u001b[?1049h")
        _ALT_SCREEN = True
    if not _CURSOR_HIDDEN:
        sys.stdout.write("\u001b[?25l")
        _CURSOR_HIDDEN = True
    sys.stdout.write("\u001b[2J\u001b[H")
    sys.stdout.flush()


@BuiltinRegistry.register("stopscreen")
def stopscreen() -> None:
    """Leave alternate screen, show cursor, restore tty."""
    global _ALT_SCREEN, _CURSOR_HIDDEN, _TTY_SAVED
    out = []
    if _ALT_SCREEN:
        out.append("\u001b[?1049l")
        _ALT_SCREEN = False
    if _CURSOR_HIDDEN:
        out.append("\u001b[?25h")
        _CURSOR_HIDDEN = False
    if out:
        sys.stdout.write("".join(out))
        sys.stdout.flush()
    if _TTY_SAVED and sys.stdin.isatty():
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _TTY_SAVED)
        _TTY_SAVED = None

@BuiltinRegistry.register("newscreen")
def newscreen() -> None:
    """Clear the screen using the terminal's alternate buffer (no scrollback)."""
    global _ALT_SCREEN
    if not _ALT_SCREEN:
        sys.stdout.write("\u001b[?1049h")
        _ALT_SCREEN = True
    sys.stdout.write("\u001b[2J\u001b[H")
    sys.stdout.flush()


@BuiltinRegistry.register("clear_line")
def clear_line() -> str:
    """Clear current line."""
    return "\u001b[2K"


@BuiltinRegistry.register("clear_to_end")
def clear_to_end() -> str:
    """Clear from cursor to end of line."""
    return "\u001b[K"


@BuiltinRegistry.register("clearbelow")
def clearbelow() -> None:
    """Clear from cursor to end of screen."""
    sys.stdout.write("\u001b[J")
    sys.stdout.flush()


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


@BuiltinRegistry.register("wait")
def wait(ms: int) -> None:
    """Wait for specified milliseconds (alias for sleep_ms)."""
    sleep_ms(ms)


def _apply_raw_mode(fd: int, flush: bool = False) -> list:
    """Switch terminal fd to raw mode. Returns old settings for restoration.

    flush=True  → TCSAFLUSH: discard pending input (good for blocking reads
                  where you want a clean slate).
    flush=False → TCSANOW:   preserve pending input (essential for non-blocking
                  reads — TCSAFLUSH would silently discard keys typed during
                  the wait/sleep between polls).
    """
    import termios
    old = termios.tcgetattr(fd)
    raw = list(old)
    raw[0] &= ~(termios.BRKINT | termios.ICRNL | termios.INPCK |
                termios.ISTRIP | termios.IXON)
    raw[1] &= ~termios.OPOST
    raw[2] &= ~(termios.CSIZE | termios.PARENB)
    raw[2] |= termios.CS8
    raw[3] &= ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
    raw[6][termios.VMIN] = 1
    raw[6][termios.VTIME] = 0
    when = termios.TCSAFLUSH if flush else termios.TCSANOW
    termios.tcsetattr(fd, when, raw)
    return old


def _read_key_unix(fd: int) -> str:
    """Read one complete key sequence from a raw file descriptor.

    Uses os.read(fd, 1) to bypass Python's TextIOWrapper buffer — the root
    cause of arrow keys appearing as bare Escape (the wrapper pre-fetches all
    three bytes but select.select sees the OS buffer as empty afterward).
    """
    import select as _sel

    ch = os.read(fd, 1).decode("latin-1")
    if ch != "\x1b":
        return _SINGLE_KEY_NORMALIZATION.get(ch, ch)

    # Read the rest of the escape sequence with a short timeout so all bytes
    # that arrived together (e.g. \x1b [ A for UpArrow) are captured.
    seq = ch
    while True:
        if _sel.select([fd], [], [], 0.05)[0]:
            next_ch = os.read(fd, 1).decode("latin-1")
            seq += next_ch
            # Standard ANSI sequences end with a letter or ~
            if len(seq) >= 3 and (next_ch.isalpha() or next_ch in "~$"):
                break
        else:
            break
    return _normalize_key(seq)

def _normalize_key(val: str) -> str:
    """Apply single-byte normalization and escape-sequence normalization."""
    val = _SINGLE_KEY_NORMALIZATION.get(val, val)
    return _ESCAPE_NORMALIZATION.get(val, val)


@BuiltinRegistry.register("key_read_nonblocking")
def key_read_nonblocking():
    """Non-blocking key read. Returns None immediately if no key is pressed."""
    if not sys.stdin.isatty():
        return None
    if os.name == "nt":
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b"\x00", b"\xe0"):
                key += msvcrt.getch()
            return _normalize_key(key.decode("latin-1"))
        return None
    else:
        import termios
        import select
        fd = sys.stdin.fileno()
        # TCSANOW preserves any input buffered during the sleep between polls
        old = _apply_raw_mode(fd, flush=False)
        try:
            if select.select([fd], [], [], 0)[0]:
                return _read_key_unix(fd)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


@BuiltinRegistry.register("key_read")
def key_read() -> str:
    """Read a single key press and return it as a string.
    For special keys (arrow keys, F-keys, etc.) the full escape sequence
    is returned so it can be matched against named key constants.
    """
    if not sys.stdin.isatty():
        raise DatarError("key_read: not a TTY")
    if os.name == "nt":
        import msvcrt
        key = msvcrt.getch()
        if key in (b"\x00", b"\xe0"):
            key += msvcrt.getch()
        return _normalize_key(key.decode("latin-1"))
    else:
        import termios
        fd = sys.stdin.fileno()
        # TCSAFLUSH discards stale input for a clean blocking read
        old = _apply_raw_mode(fd, flush=True)
        try:
            return _read_key_unix(fd)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


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

_CURSOR_HIDDEN = False
_ALT_SCREEN = False
_TTY_SAVED = None

# Ensure cursor is visible when the interpreter exits, even if a script forgot
# to show it again.
def _restore_cursor():
    out = []
    if _ALT_SCREEN:
        out.append("\u001b[?1049l")  # leave alternate screen
    if _CURSOR_HIDDEN:
        out.append("\u001b[?25h")
    if out:
        sys.stdout.write("".join(out))
        sys.stdout.flush()
    # Restore TTY modes if saved
    global _TTY_SAVED
    if _TTY_SAVED and sys.stdin.isatty():
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _TTY_SAVED)
        _TTY_SAVED = None


atexit.register(_restore_cursor)


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
