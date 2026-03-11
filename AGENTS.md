# AGENTS.md

## Project Overview
DatarScript interpreter written in pure Python 3.
- Entry point: `datarscript.py` (executable as script)
- Tests: `test_*.dtsc` (DatarScript programs) and `test_socket_server.py`
- Documentation: `datarSCRIPT.md`

## Build & Install
No compilation step required. To install command-line launchers:
```bash
python3 install.py
```
This installs `datarscript` and `dtsc` commands to `~/.local/bin` (or `/usr/local/bin` if run with sudo). Ensure the install directory is on your `PATH`.

## Linting & Formatting
This project uses **Ruff** for linting and formatting.
```bash
# Check for lint errors
ruff check .

# Auto-fix fixable issues
ruff check --fix .

# Format code (if ruff format is configured)
ruff format .
```
Configuration is in pyproject.toml if present; otherwise Ruff defaults apply.

## Testing
### Run a single DatarScript test
```bash
python3 datarscript.py test_ask_simple.dtsc
# or after install
dtsc test_ask_simple.dtsc
```
The test should exit with code 0 on success. Output is printed to stdout.

### Run all DatarScript tests
```bash
for f in test_*.dtsc; do
  echo "=== Running $f ==="
  python3 datarscript.py "$f" || { echo "FAIL: $f"; exit 1; }
done
```

### Socket integration test
1. Start the echo server in one terminal:  
   `python3 test_socket_server.py`
2. In another, run `networking_demo.dtsc` or any test that uses sockets.

## Code Style Guidelines
This codebase follows PEP 8 with a 4-space indent. Key conventions:

### Imports
- Only standard library imports.
- Group logically: `import` statements first, then `from ... import`.
- One import per line.
- Order: standard library in alphabetical order, e.g.:
  ```python
  import datetime
  import math
  import os
  import re
  import sys
  from pathlib import Path
  from copy import deepcopy
  ```

### Naming
- **Classes**: PascalCase (`DatarError`, `Env`, `Interpreter`)
- **Functions & methods**: snake_case (`preprocess`, `exec_stmt`, `_safe_comma_split`)
- **Variables**: snake_case for locals and instance attributes; constants are UPPER_SNAKE (e.g., `_END_RE`).
- **Private helpers**: prefix with a single underscore `_`.

### Types
- Use type hints on public functions/methods when they clarify intent (e.g., `def preprocess(source: str) -> list[str]`).
- Dynamic typing is accepted; annotate return types and complex parameters.
- Avoid `Any`; prefer specific types.

### Error Handling
- Custom exceptions should inherit from `Exception`. For control flow, define dedicated exceptions (`BreakSignal`, `ContinueSignal`, `ReturnSignal`).
- Use `DatarError` for interpreter/runtime errors. Include optional `lineno` for source location.
- Raise with clear, descriptive messages. Do not expose raw Python tracebacks to end users.
- Catch specific exceptions; avoid bare `except:`.

### Whitespace & Formatting
- Indent 4 spaces; never use tabs.
- No trailing whitespace.
- Blank line between top-level definitions (functions/classes) and before/after logical code sections.
- Max line length ~100 characters. Break long expressions with parentheses.

### Comments & Docstrings
- Use `#` for inline and block comments. Avoid block comments between function definitions.
- Docstrings are encouraged for all public functions, classes, and methods. Use triple-double quotes (`"""..."""`).
- Section banners (e.g., `# ════════════════════════════════════════`) separate major parts of a file.

### Regex & Patterns
- Use raw strings for regex patterns: `re.compile(r"^if\b", re.I)`.
- Compile frequently used regex patterns at module level.
- Keep patterns simple and well-commented.

## Notes
- The interpreter processes `.dtsc` files; always maintain backward compatibility with existing valid programs.
- When adding new language features, update both the parser and evaluator, and add a corresponding test in `test_*.dtsc`.
- The `install.py` script should remain POSIX-friendly; avoid Linux-only paths.
