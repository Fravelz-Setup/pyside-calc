"""Main calculator window."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QGuiApplication, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pyside_calc.engine import try_evaluate
from pyside_calc.theme import COLORS, WINDOW_WIDTH, stylesheet


@dataclass
class ResultRow:
    expression: str
    value: str

    @property
    def label(self) -> str:
        return f"{self.expression} = {self.value}"


def copy_to_clipboard(text: str) -> None:
    if shutil.which("wl-copy"):
        subprocess.run(["wl-copy"], input=text.encode(), check=False)
    else:
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
    if shutil.which("notify-send"):
        subprocess.run(
            ["notify-send", "-a", "Calc", "Resultado copiado", text],
            check=False,
        )


class CalcWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("root")
        self.setWindowTitle("Calc")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setStyleSheet(stylesheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        inputbar = QFrame()
        inputbar.setObjectName("inputbar")
        bar = QHBoxLayout(inputbar)
        bar.setContentsMargins(15, 0, 10, 0)
        bar.setSpacing(10)

        prompt = QLabel("")
        prompt.setObjectName("prompt")
        bar.addWidget(prompt)

        self.entry = QLineEdit()
        self.entry.setObjectName("entry")
        self.entry.setPlaceholderText("10+10")
        self.entry.setFrame(False)
        self.entry.textChanged.connect(self._on_text_changed)
        self.entry.returnPressed.connect(self._activate_selected)
        bar.addWidget(self.entry, stretch=1)
        root.addWidget(inputbar)

        self.results = QListWidget()
        self.results.setObjectName("results")
        self.results.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.results.itemActivated.connect(self._on_item_activated)
        self.results.itemClicked.connect(self._on_item_activated)
        root.addWidget(self.results)

        self._rows: list[ResultRow] = []
        QTimer.singleShot(0, self._center_on_screen)
        self.entry.setFocus()

    def _center_on_screen(self) -> None:
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return
        geo = screen.availableGeometry()
        self.adjustSize()
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)

    def _on_text_changed(self, text: str) -> None:
        self.results.clear()
        self._rows.clear()
        value = try_evaluate(text)
        if value is None:
            self.adjustSize()
            return
        row = ResultRow(expression=text.strip(), value=value)
        self._rows.append(row)
        item = QListWidgetItem(row.label)
        font = QFont(COLORS.get("font", "JetBrains Mono Nerd Font"), 14)
        item.setFont(font)
        self.results.addItem(item)
        self.results.setCurrentRow(0)
        self.adjustSize()
        self._center_on_screen()

    def _activate_selected(self) -> None:
        row = self.results.currentRow()
        if row < 0 or row >= len(self._rows):
            # If only one result, use it
            if len(self._rows) == 1:
                row = 0
            else:
                return
        copy_to_clipboard(self._rows[row].value)
        self.close()

    def _on_item_activated(self, item: QListWidgetItem) -> None:
        _ = item
        self._activate_selected()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        if event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Up) and self.results.count():
            self.results.keyPressEvent(event)
            return
        super().keyPressEvent(event)


def run() -> int:
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("pyside-calc")
    app.setQuitOnLastWindowClosed(True)
    win = CalcWindow()
    win.show()
    return app.exec()
