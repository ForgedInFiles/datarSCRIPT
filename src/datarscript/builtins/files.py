"""File system builtins."""

import os
from typing import Any
from .base import BuiltinRegistry
from ..errors import DatarError


@BuiltinRegistry.register("read_file")
def read_file(path: str) -> str:
    if not isinstance(path, str):
        raise DatarError("read_file: path must be a string")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise DatarError(f"read_file error: {e}")


@BuiltinRegistry.register("write_file")
def write_file(path: str, content: Any) -> str:
    if not isinstance(path, str):
        raise DatarError("write_file: path must be a string")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(content))
        return "OK"
    except Exception as e:
        raise DatarError(f"write_file error: {e}")


@BuiltinRegistry.register("list_files")
def list_files(path: str = ".") -> str:
    if not isinstance(path, str):
        raise DatarError("list_files: path must be a string")
    try:
        import json

        return json.dumps(os.listdir(path))
    except Exception as e:
        raise DatarError(f"list_files error: {e}")


@BuiltinRegistry.register("file_exists")
def file_exists(path: str) -> str:
    if not isinstance(path, str):
        raise DatarError("file_exists: path must be a string")
    try:
        import json

        return json.dumps(os.path.exists(path))
    except Exception as e:
        raise DatarError(f"file_exists error: {e}")


@BuiltinRegistry.register("mkdir")
def mkdir(path: str) -> str:
    if not isinstance(path, str):
        raise DatarError("mkdir: path must be a string")
    try:
        os.makedirs(path, exist_ok=True)
        return "Created"
    except Exception as e:
        raise DatarError(f"mkdir error: {e}")


@BuiltinRegistry.register("delete_file")
def delete_file(path: str) -> str:
    if not isinstance(path, str):
        raise DatarError("delete_file: path must be a string")
    try:
        os.remove(path)
        return "Deleted"
    except Exception as e:
        raise DatarError(f"delete_file error: {e}")
