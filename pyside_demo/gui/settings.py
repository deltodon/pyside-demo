from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsWidget(QWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.settings_layout = QVBoxLayout(self)
        self.settings_label = QLabel("TODO: Settings Widget")
        self.settings_label.setAlignment(Qt.AlignCenter)
        self.settings_layout.addWidget(self.settings_label)
