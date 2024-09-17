import sys
import os
from PySide6.QtWidgets import QApplication

from pyside_demo.gui.window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
