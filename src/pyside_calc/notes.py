"""Persist scratch notes next to the calculator."""

from __future__ import annotations

from pathlib import Path


def notes_path() -> Path:
    base = Path.home() / ".local" / "share" / "pyside-calc"
    base.mkdir(parents=True, exist_ok=True)
    return base / "notes.txt"


def load_notes() -> str:
    path = notes_path()
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def save_notes(text: str) -> None:
    path = notes_path()
    try:
        path.write_text(text, encoding="utf-8")
    except OSError:
        pass
