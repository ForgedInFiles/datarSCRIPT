"""Custom exception hierarchy for DatarScript."""

from __future__ import annotations


class DatarError(Exception):
    """Base class for all DatarScript errors."""

    def __init__(self, msg: str, lineno: int | None = None):
        self.msg = msg
        self.lineno = lineno
        super().__init__(msg)

    def __str__(self) -> str:
        where = f"line {self.lineno}" if self.lineno is not None else ""
        return f"{self.msg} ({where})" if where else self.msg


class DatarSyntaxError(DatarError):
    """Raised when source code syntax is invalid."""


class DatarNameError(DatarError):
    """Raised when an undefined variable or function is referenced."""


class DatarTypeError(DatarError):
    """Raised when an operation receives an inappropriate type."""


class DatarRuntimeError(DatarError):
    """Raised for general runtime issues not covered by more specific errors."""


class BreakSignal(Exception):
    """Signal to break out of a loop."""

    pass


class ContinueSignal(Exception):
    """Signal to continue to the next loop iteration."""

    pass


class ReturnSignal(Exception):
    """Signal to return from a function."""

    def __init__(self, val):
        self.val = val
