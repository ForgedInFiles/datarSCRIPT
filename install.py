#!/usr/bin/env python3
"""
DatarScript Installer
Sets up `datarscript` and `dtsc` commands on your system.
"""

import os
import stat
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
INTERP = SCRIPT_DIR / "datarscript.py"

# Where to install the launchers
BIN_DIRS = [
    Path.home() / ".local" / "bin",  # User-local (preferred)
    Path("/usr/local/bin"),  # System-wide (needs sudo)
]

LAUNCHER_TEMPLATE = """#!/usr/bin/env python3
import sys
sys.path.insert(0, r'{script_dir}')
from datarscript import main
main()
"""


def install():
    # Pick install dir
    bin_dir = None
    for d in BIN_DIRS:
        if d.exists() and os.access(d, os.W_OK):
            bin_dir = d
            break

    if not bin_dir:
        bin_dir = Path.home() / ".local" / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)

    print(f"Installing to: {bin_dir}")
    print(f"Interpreter:   {INTERP}\n")

    for cmd in ("datarscript", "dtsc"):
        dest = bin_dir / cmd
        launcher = LAUNCHER_TEMPLATE.format(
            cmd=cmd, interp=INTERP, script_dir=SCRIPT_DIR
        )
        dest.write_text(launcher)
        dest.chmod(dest.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print(f"  ✓ Installed: {dest}")

    print()
    # Check if bin_dir is on PATH
    path_dirs = [Path(p) for p in os.environ.get("PATH", "").split(os.pathsep)]
    if bin_dir not in path_dirs:
        shell_rc = Path.home() / ".bashrc"
        if (Path.home() / ".zshrc").exists():
            shell_rc = Path.home() / ".zshrc"
        print(f"  ⚠  {bin_dir} is not in your PATH.")
        print(f"     Add this to your {shell_rc.name}:")
        print('     export PATH="$HOME/.local/bin:$PATH"')
        print()

    print("Done! Usage:")
    print("  datarscript myprogram.dtsc")
    print("  dtsc myprogram.datar")
    print("  datarscript          (REPL mode)")


if __name__ == "__main__":
    install()
