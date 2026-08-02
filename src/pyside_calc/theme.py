"""Fixed slate/teal palette (not Rofi Catppuccin)."""

COLORS = {
    "background": "#0f1419",
    "background_alt": "#1a2332",
    "foreground": "#e8eef4",
    "selected": "#2dd4bf",
    "selected_fg": "#0f1419",
    "border": "#2dd4bf",
    "muted": "#8a9ba8",
}

WINDOW_WIDTH = 920
WINDOW_MIN_HEIGHT = 360
WINDOW_RADIUS = 14
WINDOW_BORDER_PX = 3
FONT_FAMILY = "JetBrains Mono Nerd Font"
FONT_SIZE = 20
PROMPT_SIZE = 24
RESULT_SIZE = 18
NOTES_SIZE = 16


def stylesheet() -> str:
    c = COLORS
    return f"""
    QWidget#root {{
        background-color: transparent;
    }}
    QFrame#panel {{
        background-color: {c["background"]};
        color: {c["foreground"]};
        border: {WINDOW_BORDER_PX}px solid {c["border"]};
        border-radius: {WINDOW_RADIUS}px;
        font-family: "{FONT_FAMILY}", "JetBrains Mono", monospace;
        font-size: {FONT_SIZE}px;
    }}
    QFrame#calcPane, QFrame#notesPane {{
        background-color: transparent;
        border: none;
    }}
    QFrame#divider {{
        background-color: {c["border"]};
        max-width: 2px;
        min-width: 2px;
        border: none;
        border-radius: 1px;
    }}
    QLabel#prompt {{
        color: {c["selected"]};
        background: transparent;
        font-size: {PROMPT_SIZE}px;
        font-weight: 600;
        padding-right: 6px;
    }}
    QLabel#notesTitle {{
        color: {c["selected"]};
        background: transparent;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.4px;
    }}
    QLineEdit#entry {{
        background-color: transparent;
        color: {c["foreground"]};
        border: none;
        padding: 4px 8px;
        font-size: {FONT_SIZE}px;
        font-weight: 500;
        selection-background-color: {c["selected"]};
        selection-color: {c["selected_fg"]};
    }}
    QLineEdit#entry:focus {{
        outline: none;
    }}
    QFrame#inputbar {{
        background-color: {c["background_alt"]};
        border: 1px solid {c["border"]};
        border-radius: 10px;
        min-height: 56px;
    }}
    QListWidget#results {{
        background-color: transparent;
        border: none;
        outline: none;
        color: {c["foreground"]};
        font-size: {RESULT_SIZE}px;
        padding: 0;
        min-height: 180px;
    }}
    QListWidget#results::item {{
        background-color: transparent;
        border-radius: 10px;
        padding: 12px 14px;
        margin: 3px 0;
        font-size: {RESULT_SIZE}px;
    }}
    QListWidget#results::item:selected {{
        background-color: {c["selected"]};
        color: {c["selected_fg"]};
    }}
    QListWidget#results::item:hover {{
        background-color: {c["background_alt"]};
    }}
    QTextEdit#notes {{
        background-color: {c["background_alt"]};
        color: {c["foreground"]};
        border: 1px solid {c["border"]};
        border-radius: 10px;
        padding: 12px 14px;
        font-size: {NOTES_SIZE}px;
        selection-background-color: {c["selected"]};
        selection-color: {c["selected_fg"]};
    }}
    """
