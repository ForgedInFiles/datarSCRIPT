"""Math, random, date/time builtins."""

import math
import random
import datetime
from typing import Any
from .base import BuiltinRegistry
from ..errors import DatarError


@BuiltinRegistry.register("abs")
def builtin_abs(x: float) -> float:
    return abs(x)


@BuiltinRegistry.register("round")
def builtin_round(x: float, ndigits: int = 0) -> float:
    return round(x, ndigits)


@BuiltinRegistry.register("max")
def builtin_max(*args: float) -> float:
    if not args:
        raise DatarError("max: at least one argument required")
    return max(args)


@BuiltinRegistry.register("min")
def builtin_min(*args: float) -> float:
    if not args:
        raise DatarError("min: at least one argument required")
    return min(args)


@BuiltinRegistry.register("sqrt")
def builtin_sqrt(x: float) -> float:
    if x < 0:
        raise DatarError("sqrt of negative number")
    return math.sqrt(x)


@BuiltinRegistry.register("pow")
def builtin_pow(base: float, exp: float) -> float:
    return math.pow(base, exp)


@BuiltinRegistry.register("sin")
def builtin_sin(x: float) -> float:
    return math.sin(x)


@BuiltinRegistry.register("cos")
def builtin_cos(x: float) -> float:
    return math.cos(x)


@BuiltinRegistry.register("tan")
def builtin_tan(x: float) -> float:
    return math.tan(x)


@BuiltinRegistry.register("log")
def builtin_log(x: float) -> float:
    if x <= 0:
        raise DatarError("log of non-positive number")
    return math.log(x)


@BuiltinRegistry.register("random")
def builtin_random() -> float:
    return random.random()


@BuiltinRegistry.register("randint")
def builtin_randint(a: int, b: int) -> int:
    return random.randint(a, b)


@BuiltinRegistry.register("choice")
def builtin_choice(seq: list) -> Any:
    return random.choice(seq)


@BuiltinRegistry.register("current_date")
def builtin_current_date() -> str:
    return datetime.date.today().isoformat()


@BuiltinRegistry.register("current_time")
def builtin_current_time() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


@BuiltinRegistry.register("range_inclusive")
def builtin_range_inclusive(start: int, end: int) -> list[int]:
    """Return inclusive range from start to end."""
    if start <= end:
        return list(range(start, end + 1))
    else:
        # descending
        return list(range(start, end - 1, -1))
