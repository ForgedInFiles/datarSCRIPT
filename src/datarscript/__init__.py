"""DatarScript interpreter package."""

__version__ = "2.0.0"

from .errors import (
    DatarError,
    DatarSyntaxError,
    DatarNameError,
    DatarTypeError,
    DatarRuntimeError,
    BreakSignal,
    ContinueSignal,
    ReturnSignal,
)
from .interpreter import Interpreter
