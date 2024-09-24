import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
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

from pyside_demo.gui.dialog import ConflictResolutionDialog
from pyside_demo.model.table import TableModel


class DataWidget(QWidget):
    def __init__(self, model: TableModel):
        super().__init__()
        self.model = model

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
                self.model.add_item(name, description)
            else:
                selected_items = self.item_list.selectedItems()
                if selected_items:
                    item_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                    self.model.update_item(item_id, name, description)

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
        items = self.model.get_items()
        for item in items:
            list_item = QListWidgetItem(
                f"{item['name']} ({item['sync_status']})"
            )
            list_item.setData(Qt.ItemDataRole.UserRole, item["id"])
            self.item_list.addItem(list_item)

    def load_item(self, item):
        item_id = item.data(Qt.ItemDataRole.UserRole)
        db_item = self.model.get_item_by_id(item_id)
        if db_item:
            self.name_input.setText(str(db_item["name"]))
            self.description_input.setPlainText(str(db_item["description"]))
            self.add_edit_button.setText("Update Item")

    def sync_with_postgresql(self):
        # In a real application, you would want to get these
        # from a configuration file or environment variables
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        self.model.sync_with_postgresql(host, database, user, password)
        self.resolve_conflicts()
        self.load_items()
        QMessageBox.information(
            self,
            "Sync Status",
            "Synchronization completed. Check console for details.",
        )

    def resolve_conflicts(self):
        conflict_items = self.model.get_conflict_items()

        for item in conflict_items:
            dialog = ConflictResolutionDialog(item)
            if dialog.exec_():
                resolution = dialog.get_resolution()
                self.model.resolve_conflict(item["id"], resolution)
