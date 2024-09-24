from PySide6.QtWidgets import QTableView, QVBoxLayout, QWidget

from pyside_demo.model.table import TableModel


class TableWidget(QWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.table_layout = QVBoxLayout(self)
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_view = QTableView()

        self.model = TableModel()
        self.table_view.setModel(self.model)

        self.table_view.setColumnWidth(3, 170)
        self.table_view.setColumnWidth(4, 170)
        self.table_view.setColumnWidth(5, 50)

        self.table_layout.addWidget(self.table_view)
