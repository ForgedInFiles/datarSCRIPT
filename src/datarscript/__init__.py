"""DatarScript interpreter package."""

__version__ = "0.0.1-beta.1"

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
