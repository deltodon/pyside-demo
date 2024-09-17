from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QListWidget, QMessageBox,
    QDialog, QLabel, QRadioButton, QButtonGroup, QListWidgetItem
)
from PySide6.QtCore import Qt
from database import Database, SyncStatus

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline-First PySide6 App")
        self.setGeometry(100, 100, 800, 600)

        self.db = Database()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        # Left side: Add/Edit item form
        left_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Item Description")
        self.add_edit_button = QPushButton("Add Item")
        self.add_edit_button.clicked.connect(self.add_or_edit_item)

        left_layout.addWidget(self.name_input)
        left_layout.addWidget(self.description_input)
        left_layout.addWidget(self.add_edit_button)

        # Right side: Item list and sync button
        right_layout = QVBoxLayout()
        self.item_list = QListWidget()
        self.item_list.itemClicked.connect(self.load_item)
        sync_button = QPushButton("Sync with PostgreSQL")
        sync_button.clicked.connect(self.sync_with_postgresql)

        right_layout.addWidget(self.item_list)
        right_layout.addWidget(sync_button)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        central_widget.setLayout(main_layout)

        self.load_items()

    def add_or_edit_item(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()

        if name and description:
            if self.add_edit_button.text() == "Add Item":
                self.db.add_item(name, description)
            else:
                selected_items = self.item_list.selectedItems()
                if selected_items:
                    item_id = selected_items[0].data(Qt.UserRole)
                    self.db.update_item(item_id, name, description)
            
            self.name_input.clear()
            self.description_input.clear()
            self.add_edit_button.setText("Add Item")
            self.load_items()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both name and description.")

    def load_items(self):
        self.item_list.clear()
        items = self.db.get_items()
        for item in items:
            list_item = QListWidgetItem(f"{item.name} ({item.sync_status.value})")
            list_item.setData(Qt.UserRole, item.id)
            self.item_list.addItem(list_item)

    def load_item(self, item):
        item_id = item.data(Qt.UserRole)
        session = self.db.Session()
        db_item = session.query(self.db.Item).filter_by(id=item_id).first()
        if db_item:
            self.name_input.setText(db_item.name)
            self.description_input.setPlainText(db_item.description)
            self.add_edit_button.setText("Update Item")
        session.close()

    def sync_with_postgresql(self):
        # In a real application, you would want to get these from a configuration file or environment variables
        host = "localhost"
        database = "your_database"
        user = "your_username"
        password = "your_password"

        self.db.sync_with_postgresql(host, database, user, password)
        self.resolve_conflicts()
        self.load_items()
        QMessageBox.information(self, "Sync Status", "Synchronization completed. Check console for details.")

    def resolve_conflicts(self):
        session = self.db.Session()
        conflict_items = session.query(self.db.Item).filter_by(sync_status=SyncStatus.CONFLICT).all()
        
        for item in conflict_items:
            dialog = ConflictResolutionDialog(item)
            if dialog.exec_():
                resolution = dialog.get_resolution()
                self.db.resolve_conflict(item.id, resolution)
        
        session.close()
