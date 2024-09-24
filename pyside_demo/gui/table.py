import sqlite3

import pandas as pd
from PySide6.QtWidgets import QTableView, QVBoxLayout, QWidget

from pyside_demo.db.database import SQLITE_FILE_NAME
from pyside_demo.db.sql import SQL_FETCH_ITEMS
from pyside_demo.model.table import TableModel


class TableWidget(QWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.table_layout = QVBoxLayout(self)
        self.table_view = QTableView()

        con = sqlite3.connect(SQLITE_FILE_NAME)
        data_df: pd.DataFrame = pd.read_sql_query(SQL_FETCH_ITEMS, con)

        self.model = TableModel(data_df)
        self.table_view.setModel(self.model)

        # self.table_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_layout.addWidget(self.table_view)
