from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QDialog,
    QLabel,
    QRadioButton,
    QButtonGroup,
)


class ConflictResolutionDialog(QDialog):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.setWindowTitle("Resolve Conflict")
        self.setGeometry(200, 200, 300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Conflict detected for item: {self.item.name}"))
        layout.addWidget(QLabel("Choose resolution:"))

        self.local_radio = QRadioButton("Keep local version")
        self.remote_radio = QRadioButton("Use remote version")

        button_group = QButtonGroup()
        button_group.addButton(self.local_radio)
        button_group.addButton(self.remote_radio)

        layout.addWidget(self.local_radio)
        layout.addWidget(self.remote_radio)

        resolve_button = QPushButton("Resolve")
        resolve_button.clicked.connect(self.accept)

        layout.addWidget(resolve_button)
        self.setLayout(layout)

    def get_resolution(self):
        if self.local_radio.isChecked():
            return 'local'
        elif self.remote_radio.isChecked():
            return 'remote'
        return None
