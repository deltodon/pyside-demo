from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from pyside_demo.model.table import TableModel


class TableWidget(QWidget):
    def __init__(self, model: TableModel):
        super().__init__()
        self.model = model
        self.main_layout = QVBoxLayout(self)

        # Table view
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        # Make the table read-only
        self.table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Adjust column widths
        self.table_view.setColumnWidth(0, 100)  # ID
        self.table_view.setColumnWidth(1, 120)  # Name
        self.table_view.setColumnWidth(2, 120)  # Description
        self.table_view.setColumnWidth(3, 120)  # Created At
        self.table_view.setColumnWidth(4, 120)  # Updated At
        self.table_view.setColumnWidth(5, 50)  # Version
        self.table_view.setColumnWidth(6, 70)  # Sync Status

        self.main_layout.addWidget(self.table_view)
        self.setLayout(self.main_layout)

    def refresh(self):
        self.model.refresh_data()
