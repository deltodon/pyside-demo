import sys

from PySide6.QtWidgets import QApplication

from pyside_demo.gui.theme import set_dark_mode
from pyside_demo.gui.window import MainWindow

# sys.argv += ['-platform', 'windows:darkmode=2']


def main():
    app = QApplication(sys.argv)
    set_dark_mode(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
