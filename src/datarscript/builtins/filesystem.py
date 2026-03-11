"""File system operations builtins for DatarScript."""

import os
import shutil
from pathlib import Path
from .base import BuiltinRegistry
from ..errors import DatarError


@BuiltinRegistry.register("read_file")
def read_file(path: str) -> str:
    """Read contents of a file."""
    if not isinstance(path, str):
        raise DatarError("read_file: path must be a string")
    try:
        p = Path(path).expanduser()
        if not p.exists():
            raise DatarError(f"File not found: {path}")
        if not p.is_file():
            raise DatarError(f"Not a file: {path}")
        return p.read_text(encoding="utf-8")
    except PermissionError:
        raise DatarError(f"Permission denied: {path}")
    except Exception as e:
        raise DatarError(f"Error reading file: {str(e)}")


@BuiltinRegistry.register("write_file")
def write_file(path: str, content: str) -> str:
    """Write content to a file (creates or overwrites)."""
    if not isinstance(path, str):
        raise DatarError("write_file: path must be a string")
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {path}"
    except PermissionError:
        raise DatarError(f"Permission denied: {path}")
    except Exception as e:
        raise DatarError(f"Error writing file: {str(e)}")


@BuiltinRegistry.register("append_file")
def append_file(path: str, content: str) -> str:
    """Append content to a file."""
    if not isinstance(path, str):
        raise DatarError("append_file: path must be a string")
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully appended to {path}"
    except PermissionError:
        raise DatarError(f"Permission denied: {path}")
    except Exception as e:
        raise DatarError(f"Error appending to file: {str(e)}")


@BuiltinRegistry.register("delete_file")
def delete_file(path: str) -> str:
    """Delete a file."""
    if not isinstance(path, str):
        raise DatarError("delete_file: path must be a string")
    try:
        p = Path(path).expanduser()
        if not p.exists():
            raise DatarError(f"File not found: {path}")
        if not p.is_file():
            raise DatarError(f"Not a file: {path}")
        p.unlink()
        return f"Successfully deleted {path}"
    except PermissionError:
        raise DatarError(f"Permission denied: {path}")
    except Exception as e:
        raise DatarError(f"Error deleting file: {str(e)}")


@BuiltinRegistry.register("list_files")
def list_files(path: str = ".") -> list:
    """List files and directories in a path."""
    if not isinstance(path, str):
        raise DatarError("list_files: path must be a string")
    try:
        p = Path(path).expanduser()
        if not p.exists():
            raise DatarError(f"Path not found: {path}")
        if not p.is_dir():
            raise DatarError(f"Not a directory: {path}")
        items = []
        for item in sorted(p.iterdir()):
            item_type = "dir" if item.is_dir() else "file"
            items.append({"name": item.name, "type": item_type, "path": str(item)})
        return items
    except PermissionError:
        raise DatarError(f"Permission denied: {path}")
    except Exception as e:
        raise DatarError(f"Error listing files: {str(e)}")


@BuiltinRegistry.register("create_dir")
def create_dir(path: str) -> str:
    """Create a directory (including parent directories)."""
    if not isinstance(path, str):
        raise DatarError("create_dir: path must be a string")
    try:
        p = Path(path).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return f"Successfully created directory {path}"
    except PermissionError:
        raise DatarError(f"Permission denied: {path}")
    except Exception as e:
        raise DatarError(f"Error creating directory: {str(e)}")


@BuiltinRegistry.register("delete_dir")
def delete_dir(path: str) -> str:
    """Delete a directory (must be empty)."""
    if not isinstance(path, str):
        raise DatarError("delete_dir: path must be a string")
    try:
        p = Path(path).expanduser()
        if not p.exists():
            raise DatarError(f"Directory not found: {path}")
        if not p.is_dir():
            raise DatarError(f"Not a directory: {path}")
        p.rmdir()
        return f"Successfully deleted directory {path}"
    except OSError:
        raise DatarError(f"Directory not empty: {path}")
    except Exception as e:
        raise DatarError(f"Error deleting directory: {str(e)}")


@BuiltinRegistry.register("file_exists")
def file_exists(path: str) -> bool:
    """Check if a file or directory exists."""
    if not isinstance(path, str):
        raise DatarError("file_exists: path must be a string")
    p = Path(path).expanduser()
    return p.exists()


@BuiltinRegistry.register("is_file")
def is_file(path: str) -> bool:
    """Check if path is a file."""
    if not isinstance(path, str):
        raise DatarError("is_file: path must be a string")
    p = Path(path).expanduser()
    return p.is_file()


@BuiltinRegistry.register("is_dir")
def is_dir(path: str) -> bool:
    """Check if path is a directory."""
    if not isinstance(path, str):
        raise DatarError("is_dir: path must be a string")
    p = Path(path).expanduser()
    return p.is_dir()


@BuiltinRegistry.register("get_cwd")
def get_cwd() -> str:
    """Get current working directory."""
    return os.getcwd()


@BuiltinRegistry.register("set_cwd")
def set_cwd(path: str) -> str:
    """Change current working directory."""
    if not isinstance(path, str):
        raise DatarError("set_cwd: path must be a string")
    try:
        os.chdir(Path(path).expanduser())
        return os.getcwd()
    except Exception as e:
        raise DatarError(f"Error changing directory: {str(e)}")


@BuiltinRegistry.register("copy_file")
def copy_file(src: str, dst: str) -> str:
    """Copy a file from src to dst."""
    if not isinstance(src, str) or not isinstance(dst, str):
        raise DatarError("copy_file: paths must be strings")
    try:
        shutil.copy2(Path(src).expanduser(), Path(dst).expanduser())
        return f"Copied {src} to {dst}"
    except Exception as e:
        raise DatarError(f"Error copying file: {str(e)}")


@BuiltinRegistry.register("move_file")
def move_file(src: str, dst: str) -> str:
    """Move a file from src to dst."""
    if not isinstance(src, str) or not isinstance(dst, str):
        raise DatarError("move_file: paths must be strings")
    try:
        shutil.move(Path(src).expanduser(), Path(dst).expanduser())
        return f"Moved {src} to {dst}"
    except Exception as e:
        raise DatarError(f"Error moving file: {str(e)}")


@BuiltinRegistry.register("get_file_size")
def get_file_size(path: str) -> int:
    """Get file size in bytes."""
    if not isinstance(path, str):
        raise DatarError("get_file_size: path must be a string")
    try:
        return Path(path).expanduser().stat().st_size
    except Exception as e:
        raise DatarError(f"Error getting file size: {str(e)}")
