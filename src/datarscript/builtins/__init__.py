"""Builtins package: import all modules to register their builtins."""

# Import all builtin modules to trigger registration via BuiltinRegistry
from . import files  # noqa: F401
from . import filesystem  # noqa: F401
from . import http  # noqa: F401
from . import http_json  # noqa: F401
from . import math_stdlib  # noqa: F401
from . import system  # noqa: F401
from . import terminal  # noqa: F401

# Graphics builtins are optional; only import if PySide6 available
try:
    from . import graphics  # noqa: F401
except Exception:
    # PySide6 not installed; graphics builtins will raise when called
    pass
