# AGENTS.md

## Project Overview
DatarScript interpreter written in pure Python 3.
- Entry point: `datarscript.py` (executable as script)
- Tests: `test_*.dtsc` (DatarScript programs) and `test_socket_server.py`
- Documentation: `datarSCRIPT.md`
- Source code: Located in `src/datarscript/` directory
- Built-in modules: Located in `src/datarscript/builtins/`
- Core components: Lexer, Parser, AST, Interpreter, Error handling

## Build & Install
No compilation step required. To install command-line launchers:
```bash
python3 install.py
```
This installs `datarscript` and `dtsc` commands to `~/.local/bin` (or `/usr/local/bin` if run with sudo). Ensure the install directory is on your `PATH`.

For development, you can run the interpreter directly:
```bash
python3 datarscript.py
```
Or use the installed command:
```bash
datarscript
```

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
Additional tools:
- Black is configured via pyproject.toml (line-length=88) but Ruff handles formatting
- isort is configured via pyproject.toml (profile="black")

To verify formatting is correct:
```bash
ruff check --diff .
```

## Testing
### Run a single DatarScript test
```bash
python3 datarscript.py tests/01_hello_world.dtsc
# or after install
dtsc tests/01_hello_world.dtsc
```
The test should exit with code 0 on success. Output is printed to stdout.

### Run all DatarScript tests
```bash
for f in tests/test_*.dtsc; do
  echo "=== Running $f ==="
  python3 datarscript.py "$f" || { echo "FAIL: $f"; exit 1; }
done
```
For non-test .dtsc files in tests/:
```bash
for f in tests/*.dtsc; do
  echo "=== Running $f ==="
  python3 datarscript.py "$f" || { echo "FAIL: $f"; exit 1; }
done
```

### Socket integration test
1. Start the echo server in one terminal:  
   `python3 test_socket_server.py`
2. In another, run any test that uses sockets (e.g., `tests/test_blocking_input.dtsc`).

### Test structure
- Unit tests for Python modules are in `tests/` directory (if any)
- DatarScript language tests are `.dtsc` files in `tests/` directory
- Socket-related tests: `test_socket_server.py` and corresponding `.dtsc` tests
- Test files follow naming convention: `test_*.dtsc` for language tests, `*_test.dtsc` for specific feature tests

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
- Relative imports are not used (flat structure within src/datarscript/)

### Naming
- **Classes**: PascalCase (`DatarError`, `Env`, `Interpreter`)
- **Functions & methods**: snake_case (`preprocess`, `exec_stmt`, `_safe_comma_split`)
- **Variables**: snake_case for locals and instance attributes; constants are UPPER_SNAKE (e.g., `_END_RE`).
- **Private helpers**: prefix with a single underscore `_`.
- **Module-level constants**: UPPER_SNAKE_CASE with leading underscore if private (`_VERSION`)

### Types
- Use type hints on public functions/methods when they clarify intent (e.g., `def preprocess(source: str) -> list[str]`).
- Dynamic typing is accepted; annotate return types and complex parameters.
- Avoid `Any`; prefer specific types.
- For function arguments with complex types, use `typing` module (e.g., `List[str]`, `Dict[str, int]`, `Optional[Tuple[int, str]]`).
- Return types should always be annotated for public APIs.

### Error Handling
- Custom exceptions should inherit from `Exception`. For control flow, define dedicated exceptions (`BreakSignal`, `ContinueSignal`, `ReturnSignal`).
- Use `DatarError` for interpreter/runtime errors. Include optional `lineno` for source location.
- Raise with clear, descriptive messages. Do not expose raw Python tracebacks to end users.
- Catch specific exceptions; avoid bare `except:`.
- When re-raising, use `raise` without arguments to preserve traceback, or `raise ... from ...` for chaining.
- All interpreter errors should derive from `DatarError` defined in `errors.py`.

### Whitespace & Formatting
- Indent 4 spaces; never use tabs.
- No trailing whitespace.
- Blank line between top-level definitions (functions/classes) and before/after logical code sections.
- Max line length ~88 characters (as per Ruff/Black configuration). Break long expressions with parentheses.
- Use vertical alignment sparingly and only when it improves readability.
- Import statements should not exceed 4 lines; group related imports.

### Comments & Docstrings
- Use `#` for inline and block comments. Avoid block comments between function definitions.
- Docstrings are encouraged for all public functions, classes, and methods. Use triple-double quotes (`"""..."""`).
- Section banners (e.g., `# ═════════════════════════════════════════`) separate major parts of a file.
- Docstrings should follow the Napoleon style (Google-style) or reST style for consistency.
- Function docstrings should include Args, Returns, and Raises sections when applicable.
- TODO comments should include a ticket or owner if possible: `# TODO(username): description`

### Regex & Patterns
- Use raw strings for regex patterns: `re.compile(r"^if\b", re.I)`.
- Compile frequently used regex patterns at module level.
- Keep patterns simple and well-commented.
- For complex patterns, consider using `re.VERBOSE` flag and inline comments.
- Prefer string methods over regex when possible (startswith, endswith, in, etc.).

## Development Workflow
### Setting up development environment
1. Fork and clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install in development mode: `pip install -e .`
5. Install pre-commit hooks (if applicable): `pre-commit install`

### Running tests
- Run the test suite: `python3 -m pytest tests/` (if pytest is configured) or use the shell loop above
- For quick validation during development, run individual test files
- To run tests with coverage (if configured): `python3 -m pytest --cov=src tests/`

### Linting and formatting
- Run linting: `ruff check .`
- Run formatter: `ruff format .`
- Fix lint errors automatically: `ruff check --fix .`
- Check for type consistency (if using mypy): `mypy src/` (if configured)

### Making changes
1. Create a new branch for your feature/fix
2. Make changes, adhering to the code style guidelines
3. Add or update tests as necessary
4. Run linting and tests to ensure nothing is broken
5. Commit with a clear, descriptive message
6. Push to your fork and open a pull request

### Repository Structure
- `/` - Root directory
- `/src/datarscript/` - Main Python package
- `/src/datarscript/builtins/` - Built-in function modules
- `/tests/` - Test files (.dtsc scripts and Python test helpers)
- `/docs/` - Documentation files
- `/dist/` - Distribution files (created by build process)
- `datarscript.py` - Entry point script
- `install.py` - Installation script
- `test_socket_server.py` - Socket test server
- `pyproject.toml` - Build system and tool configuration
- `README.md` - Project overview
- `datarSCRIPT.md` - Language specification
- `LICENSE` - License file
- `.gitignore` - Git ignore rules
- `.ruff_cache/` - Ruff cache directory
- `__pycache__/` - Python bytecode cache

## Notes
- The interpreter processes `.dtsc` files; always maintain backward compatibility with existing valid programs.
- When adding new language features, update both the parser and evaluator, and add a corresponding test in `tests/test_*.dtsc`.
- The `install.py` script should remain POSIX-friendly; avoid Linux-only paths.
- Keep dependencies minimal; only use standard library unless absolutely necessary.
- When in doubt about a design decision, refer to existing code patterns in the codebase.
- All user-facing strings should be suitable for internationalization (though not currently implemented).
- Performance considerations: Avoid expensive operations in frequently called lexer/parser functions.