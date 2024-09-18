from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


def set_dark_mode(app: QApplication):
    dark_palette: QPalette = app.palette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(
        QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127)
    )
    dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(
        QPalette.Disabled, QPalette.Text, QColor(127, 127, 127)
    )
    dark_palette.setColor(QPalette.Dark, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(
        QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127)
    )
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(
        QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80)
    )
    dark_palette.setColor(QPalette.HighlightedText, Qt.white)
    dark_palette.setColor(
        QPalette.Disabled,
        QPalette.HighlightedText,
        QColor(127, 127, 127),
    )
    dark_palette.setColor(QPalette.PlaceholderText, QColor(127, 127, 127))

    app.setStyle("Fusion")
    app.setPalette(dark_palette)

    # return dark_palette
