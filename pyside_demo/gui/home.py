from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HomeDashboard(QWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.home_layout = QVBoxLayout(self)
        self.home_label = QLabel("TODO: Home Dashboard")
        self.home_label.setStyleSheet(
            """
            QLabel {
                color: white;
            }
        """
        )
        self.home_label.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(self.home_label)
