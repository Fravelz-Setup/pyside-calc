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
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pyside_calc.engine import try_evaluate
from pyside_calc.notes import load_notes, save_notes
from pyside_calc.theme import (
    FONT_FAMILY,
    FONT_SIZE,
    NOTES_SIZE,
    RESULT_SIZE,
    WINDOW_MIN_HEIGHT,
    WINDOW_WIDTH,
    stylesheet,
)


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
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setMinimumHeight(WINDOW_MIN_HEIGHT)
        self.setStyleSheet(stylesheet())

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(400)
        self._save_timer.timeout.connect(self._persist_notes)

        shell = QVBoxLayout(self)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)

        panel = QFrame()
        panel.setObjectName("panel")
        shell.addWidget(panel)

        body = QHBoxLayout(panel)
        body.setContentsMargins(22, 22, 22, 22)
        body.setSpacing(16)

        # --- Left: calculator ---
        calc_pane = QFrame()
        calc_pane.setObjectName("calcPane")
        calc_pane.setMinimumWidth(360)
        calc_layout = QVBoxLayout(calc_pane)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        calc_layout.setSpacing(14)

        inputbar = QFrame()
        inputbar.setObjectName("inputbar")
        bar = QHBoxLayout(inputbar)
        bar.setContentsMargins(16, 10, 12, 10)
        bar.setSpacing(12)

        prompt = QLabel("")
        prompt.setObjectName("prompt")
        bar.addWidget(prompt)

        self.entry = QLineEdit()
        self.entry.setObjectName("entry")
        self.entry.setPlaceholderText("10+10")
        self.entry.setFrame(False)
        self.entry.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        self.entry.textChanged.connect(self._on_text_changed)
        self.entry.returnPressed.connect(self._activate_selected)
        bar.addWidget(self.entry, stretch=1)
        calc_layout.addWidget(inputbar)

        self.results = QListWidget()
        self.results.setObjectName("results")
        self.results.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.results.setFont(QFont(FONT_FAMILY, RESULT_SIZE))
        self.results.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.results.itemActivated.connect(self._on_item_activated)
        self.results.itemClicked.connect(self._on_item_activated)
        calc_layout.addWidget(self.results, stretch=1)

        body.addWidget(calc_pane, stretch=5)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.Shape.VLine)
        body.addWidget(divider)

        # --- Right: notes ---
        notes_pane = QFrame()
        notes_pane.setObjectName("notesPane")
        notes_pane.setMinimumWidth(320)
        notes_layout = QVBoxLayout(notes_pane)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(10)

        notes_title = QLabel("Notas")
        notes_title.setObjectName("notesTitle")
        notes_layout.addWidget(notes_title)

        self.notes = QTextEdit()
        self.notes.setObjectName("notes")
        self.notes.setPlaceholderText("Escribe aquí…")
        self.notes.setFont(QFont(FONT_FAMILY, NOTES_SIZE))
        self.notes.setAcceptRichText(False)
        self.notes.setPlainText(load_notes())
        self.notes.textChanged.connect(self._schedule_save_notes)
        notes_layout.addWidget(self.notes, stretch=1)

        body.addWidget(notes_pane, stretch=5)

        self._rows: list[ResultRow] = []
        QTimer.singleShot(0, self._center_on_screen)
        self.entry.setFocus()

    def _schedule_save_notes(self) -> None:
        self._save_timer.start()

    def _persist_notes(self) -> None:
        save_notes(self.notes.toPlainText())

    def closeEvent(self, event) -> None:  # noqa: ANN001
        self._save_timer.stop()
        self._persist_notes()
        super().closeEvent(event)

    def _center_on_screen(self) -> None:
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return
        geo = screen.availableGeometry()
        self.adjustSize()
        if self.height() < WINDOW_MIN_HEIGHT:
            self.resize(WINDOW_WIDTH, WINDOW_MIN_HEIGHT)
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)

    def _on_text_changed(self, text: str) -> None:
        self.results.clear()
        self._rows.clear()
        value = try_evaluate(text)
        if value is None:
            return
        row = ResultRow(expression=text.strip(), value=value)
        self._rows.append(row)
        item = QListWidgetItem(row.label)
        item.setFont(QFont(FONT_FAMILY, RESULT_SIZE))
        self.results.addItem(item)
        self.results.setCurrentRow(0)

    def _activate_selected(self) -> None:
        row = self.results.currentRow()
        if row < 0 or row >= len(self._rows):
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
        # Arrow keys only when focus is on the calc entry, not while editing notes
        if (
            self.entry.hasFocus()
            and event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Up)
            and self.results.count()
        ):
            self.results.keyPressEvent(event)
            return
        super().keyPressEvent(event)


def run() -> int:
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("pyside-calc")
    app.setQuitOnLastWindowClosed(True)
    app.setFont(QFont(FONT_FAMILY, FONT_SIZE))
    win = CalcWindow()
    win.show()
    return app.exec()
