import sys

from PySide6.QtWidgets import QApplication

from pyside_demo.gui.window import MainWindow
from pyside_demo.theme import set_theme


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    set_theme(app, "dark")

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
