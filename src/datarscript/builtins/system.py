"""System builtins."""

import os
from .base import BuiltinRegistry
from ..errors import DatarError, DatarRuntimeError


@BuiltinRegistry.register("input")
def builtin_input(prompt: str = "") -> str:
    """Read a line from standard input."""
    return input(prompt)


@BuiltinRegistry.register("trim")
def builtin_trim(s: str) -> str:
    """Trim whitespace from a string."""
    if not isinstance(s, str):
        raise DatarError("trim: argument must be a string")
    return s.strip()


@BuiltinRegistry.register("builtin_raise")
def builtin_raise(error_type: str, message: str) -> None:
    """Raise a Datar error with the given message."""
    raise DatarRuntimeError(f"{error_type}: {message}")


@BuiltinRegistry.register("get_current_directory")
def get_cwd() -> str:
    return os.getcwd()


@BuiltinRegistry.register("set_current_directory")
def set_cwd(path: str) -> str:
    if not isinstance(path, str):
        raise DatarError("set_current_directory: path must be a string")
    os.chdir(path)
    return os.getcwd()


@BuiltinRegistry.register("exit")
def builtin_exit(code: int = 0) -> None:
    raise SystemExit(code)


@BuiltinRegistry.register("print")
def builtin_print(*args, sep: str = " ", end: str = "\n") -> str:
    output = sep.join(str(a) for a in args) + end
    print(output, end="", flush=True)
    return output


@BuiltinRegistry.register("key_repr")
def key_repr(s) -> str:
    """Return a safe printable representation of any string (shows escape sequences)."""
    return repr(s)


@BuiltinRegistry.register("key_codes")
def key_codes(s) -> str:
    """Return the hex byte codes of a string, space-separated. Useful for debugging key presses."""
    if not isinstance(s, str):
        return "(not a string)"
    return " ".join(f"{ord(c):02x}" for c in s)


@BuiltinRegistry.register("chr")
def builtin_chr(code: int) -> str:
    """Return the character for the given ASCII code."""
    if not isinstance(code, int):
        raise DatarError("chr: argument must be an integer")
    return chr(code)


@BuiltinRegistry.register("ord")
def builtin_ord(char: str) -> int:
    """Return the ASCII code for the given character."""
    if not isinstance(char, str) or len(char) != 1:
        raise DatarError("ord: argument must be a single character")
    return ord(char)
