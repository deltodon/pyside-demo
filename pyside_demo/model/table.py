import sqlite3
from typing import Any, Union

import pandas as pd
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from pyside_demo.db.database import SQLITE_FILE_NAME
from pyside_demo.db.sql import SQL_FETCH_ITEMS


class TableModel(QAbstractTableModel):

    def __init__(self):
        super(TableModel, self).__init__()
        con = sqlite3.connect(SQLITE_FILE_NAME)
        self._data: pd.DataFrame = pd.read_sql_query(SQL_FETCH_ITEMS, con)

    def data(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        return None

    def rowCount(
        self, parent: Union[QModelIndex, QPersistentModelIndex] = QModelIndex()
    ) -> int:
        return self._data.shape[0]

    def columnCount(
        self, parent: Union[QModelIndex, QPersistentModelIndex] = QModelIndex()
    ) -> int:
        return self._data.shape[1]

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None
