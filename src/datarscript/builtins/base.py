"""Builtin function registry."""

from __future__ import annotations

from typing import Callable, Dict


class Builtin:
    def __init__(self, name: str, func: Callable, signature: dict | None = None):
        self.name = name
        self.func = func
        self.signature = signature or {}

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class BuiltinRegistry:
    _registry: Dict[str, Builtin] = {}

    @classmethod
    def register(cls, name: str, signature: dict | None = None):
        def decorator(func: Callable):
            cls._registry[name] = Builtin(name, func, signature)
            return func

        return decorator

    @classmethod
    def get_all(cls) -> Dict[str, Builtin]:
        return dict(cls._registry)

    @classmethod
    def get(cls, name: str) -> Builtin | None:
        return cls._registry.get(name)

    @classmethod
    def clear(cls):
        cls._registry.clear()
