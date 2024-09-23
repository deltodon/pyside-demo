from PySide6.QtCore import Qt
from PySide6.QtWidgets import (  # QLabel,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pyside_demo.db.database import Database, Item, SyncStatus
from pyside_demo.gui.dialog import ConflictResolutionDialog


class DataWidget(QWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.db = Database()

        self.main_layout = QHBoxLayout(self)

        # Left side: Add/Edit item form
        self.left_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Item Description")
        self.add_edit_button = QPushButton("Add Item")
        self.add_edit_button.clicked.connect(self.add_or_edit_item)

        self.left_layout.addWidget(self.name_input)
        self.left_layout.addWidget(self.description_input)
        self.left_layout.addWidget(self.add_edit_button)

        # Right side: Item list and sync button
        self.right_layout = QVBoxLayout()
        self.item_list = QListWidget()
        self.item_list.itemClicked.connect(self.load_item)
        sync_button = QPushButton("Sync with PostgreSQL")
        sync_button.clicked.connect(self.sync_with_postgresql)

        self.right_layout.addWidget(self.item_list)
        self.right_layout.addWidget(sync_button)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

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
                    item_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                    self.db.update_item(item_id, name, description)

            self.name_input.clear()
            self.description_input.clear()
            self.add_edit_button.setText("Add Item")
            self.load_items()
        else:
            QMessageBox.warning(
                self, "Input Error", "Please enter both name and description."
            )

    def load_items(self):
        self.item_list.clear()
        items = self.db.get_items()
        for item in items:
            list_item = QListWidgetItem(
                f"{item.name} ({item.sync_status.value})"
            )
            list_item.setData(Qt.ItemDataRole.UserRole, item.id)
            self.item_list.addItem(list_item)

    def load_item(self, item):
        item_id = item.data(Qt.ItemDataRole.UserRole)
        session = self.db.Session()
        db_item = session.query(Item).filter_by(id=item_id).first()
        if db_item:
            self.name_input.setText(str(db_item.name))
            self.description_input.setPlainText(str(db_item.description))
            self.add_edit_button.setText("Update Item")
        session.close()

    def sync_with_postgresql(self):
        # In a real application, you would want to get these
        # from a configuration file or environment variables
        host = "localhost"
        database = "your_database"
        user = "your_username"
        password = "your_password"

        self.db.sync_with_postgresql(host, database, user, password)
        self.resolve_conflicts()
        self.load_items()
        QMessageBox.information(
            self,
            "Sync Status",
            "Synchronization completed. Check console for details.",
        )

    def resolve_conflicts(self):
        session = self.db.Session()
        conflict_items = (
            session.query(Item)
            .filter_by(sync_status=SyncStatus.CONFLICT)
            .all()
        )

        for item in conflict_items:
            dialog = ConflictResolutionDialog(item)
            if dialog.exec_():
                resolution = dialog.get_resolution()
                self.db.resolve_conflict(item.id, resolution)

        session.close()
