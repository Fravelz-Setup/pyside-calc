"""Fixed slate/teal palette (not Rofi Catppuccin)."""

COLORS = {
    "background": "#0f1419",
    "background_alt": "#1a2332",
    "foreground": "#d8e1e8",
    "selected": "#2dd4bf",
    "selected_fg": "#0f1419",
    "border": "#3d4f5f",
    "muted": "#6b7c8a",
}

WINDOW_WIDTH = 520
WINDOW_RADIUS = 15
FONT_FAMILY = "JetBrains Mono Nerd Font"
FONT_SIZE = 14


def stylesheet() -> str:
    c = COLORS
    return f"""
    QWidget#root {{
        background-color: {c["background"]};
        color: {c["foreground"]};
        border: 2px solid {c["border"]};
        border-radius: {WINDOW_RADIUS}px;
        font-family: "{FONT_FAMILY}", "JetBrains Mono", monospace;
        font-size: {FONT_SIZE}px;
    }}
    QLabel#prompt {{
        color: {c["foreground"]};
        background: transparent;
        font-size: 18px;
        padding-right: 4px;
    }}
    QLineEdit#entry {{
        background-color: {c["background_alt"]};
        color: {c["foreground"]};
        border: none;
        border-radius: 10px;
        padding: 15px 12px;
        selection-background-color: {c["selected"]};
        selection-color: {c["selected_fg"]};
    }}
    QLineEdit#entry:focus {{
        outline: none;
    }}
    QFrame#inputbar {{
        background-color: {c["background_alt"]};
        border-radius: 10px;
    }}
    QListWidget#results {{
        background-color: transparent;
        border: none;
        outline: none;
        color: {c["foreground"]};
        padding: 0;
    }}
    QListWidget#results::item {{
        background-color: transparent;
        border-radius: 10px;
        padding: 10px 12px;
        margin: 2px 0;
    }}
    QListWidget#results::item:selected {{
        background-color: {c["selected"]};
        color: {c["selected_fg"]};
    }}
    QListWidget#results::item:hover {{
        background-color: {c["background_alt"]};
    }}
    """
