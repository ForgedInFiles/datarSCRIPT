#!/usr/bin/env python3
"""
DatarScript Interpreter v2.0
A natural language programming language with proper lexer, parser, and modular builtins.

Usage:
  python3 -m datarscript <file.dtsc>
  datarscript <file.dtsc>
  dtsc <file.dtsc>
"""

import sys
from pathlib import Path

# Allow running as `python3 -m datarscript` or via installed script
try:
    from src.datarscript.interpreter import Interpreter
except ImportError:
    # If installed as package
    from datarscript.interpreter import Interpreter


def run_file(path: str) -> None:
    p = Path(path)
    if not p.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    source = p.read_text(encoding="utf-8")
    interp = Interpreter()
    try:
        interp.run(source)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(1)


def run_repl() -> None:
    print("DatarScript REPL (0.0.1-beta.1) – type 'quit.' or Ctrl+C to exit")
    interp = Interpreter()
    buf = []
    while True:
        try:
            line = input(">>> ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if line.strip().lower() in ("quit.", "exit.", "quit", "exit"):
            break
        buf.append(line)
        source = "\n".join(buf)
        # Simple check: if line ends with '.' and no open blocks?
        if line.strip().endswith("."):
            try:
                interp.run(source)
                buf = []
            except Exception as e:
                print(f"[Error] {e}")
                buf = []
        else:
            # continue accumulating lines
            pass


def main() -> None:
    argv = sys.argv[1:]
    if not argv:
        run_repl()
        return
    if argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] in ("-v", "--version"):
        print("DatarScript Interpreter 0.0.1-beta.1")
        return
    run_file(argv[0])


if __name__ == "__main__":
    main()
