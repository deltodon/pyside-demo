import os

from PySide6.QtWidgets import QApplication

THEME_DIR: str = os.path.dirname(os.path.abspath(__file__))


def set_theme(app: QApplication, theme_name: str):
    with open(f"{THEME_DIR}/{theme_name}.qss", "r") as f:
        theme: str = f.read()
        app.setStyleSheet(theme)
