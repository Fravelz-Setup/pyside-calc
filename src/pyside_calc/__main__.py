"""CLI entry: python -m pyside_calc"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    # Allow running without install: repo/src on sys.path
    src = Path(__file__).resolve().parents[1]
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def main() -> None:
    _ensure_src_on_path()
    from pyside_calc.app import run

    raise SystemExit(run())


if __name__ == "__main__":
    main()
