from typing import Any, Dict, List, Union

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from pyside_demo.db.database import Database, Item, SyncStatus


class TableModel(QAbstractTableModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.db = Database()
        self._data: List[Item] = []
        self._headers = [
            "ID",
            "Name",
            "Description",
            "Created At",
            "Updated At",
            "Version",
            "Sync Status",
        ]
        self.refresh_data()

    def refresh_data(self):
        self._data = self.db.get_items()
        self.layoutChanged.emit()

    def data(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            item = self._data[index.row()]
            column = index.column()
            if column == 0:
                return str(item.id)
            elif column == 1:
                return str(item.name)
            elif column == 2:
                return str(item.description)
            elif column == 3:
                return item.created_at.strftime("%Y-%m-%d %H:%M:%S")
            elif column == 4:
                return item.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            elif column == 5:
                return str(item.version)
            elif column == 6:
                return str(item.sync_status.value)
        return None

    def rowCount(
        self, parent: Union[QModelIndex, QPersistentModelIndex] = QModelIndex()
    ) -> int:
        return len(self._data)

    def columnCount(
        self, parent: Union[QModelIndex, QPersistentModelIndex] = QModelIndex()
    ) -> int:
        return len(self._headers)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self._headers[section]
        return None

    def add_item(self, name: str, description: str):
        self.db.add_item(name, description)
        self.refresh_data()

    def update_item(self, item_id: str, name: str, description: str):
        self.db.update_item(item_id, name, description)
        self.refresh_data()

    def get_items(self) -> List[Dict[str, Any]]:
        return [self.item_to_dict(item) for item in self._data]

    def get_item_by_id(self, item_id: str) -> Union[Dict[str, Any], None]:
        for item in self._data:
            if item.id == item_id:
                return self.item_to_dict(item)
        return None

    def item_to_dict(self, item: Item) -> Dict[str, Any]:
        return {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
            "version": item.version,
            "sync_status": item.sync_status.value,
        }

    def sync_with_postgresql(self):
        self.db.sync_with_postgresql()
        self.refresh_data()

    def get_conflict_items(self) -> List[Dict[str, Any]]:
        return [
            self.item_to_dict(item)
            for item in self._data
            if item.sync_status == SyncStatus.CONFLICT
        ]

    def resolve_conflict(self, item_id: str, resolution_choice: str):
        self.db.resolve_conflict(item_id, resolution_choice)
        self.refresh_data()
