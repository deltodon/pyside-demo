from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from pyside_demo.db.database import Database, Item, SyncStatus
from pyside_demo.db.sql import (
    SQL_CHECK_FOR_CONFLICTS,
    SQL_CREATE_TABLE,
    SQL_FETCH_ITEMS,
    SQL_UPDATE_OR_INSERT_ITEM,
)


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def database():
    with patch("pyside_demo.db.database.create_engine"), patch(
        "pyside_demo.db.database.Base.metadata.create_all"
    ), patch("pyside_demo.db.database.sessionmaker"):
        return Database()


@pytest.fixture
def mock_postgres_connection():
    mock_conn = Mock()
    mock_cur = Mock()
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = []  # Default to empty list
    mock_cur.fetchone.return_value = None  # Default to None
    return mock_conn, mock_cur


@pytest.fixture
def mock_item():
    item = Mock(spec=Item)
    item.sync_status = SyncStatus.MODIFIED
    item.id = "test_id"
    item.name = "Test Item"
    item.description = "Test Description"
    item.created_at = datetime(2023, 1, 1, 12, 0, 0)
    item.updated_at = datetime(2023, 1, 1, 12, 0, 0)
    item.version = 1
    return item


@pytest.mark.usefixtures("database")
class TestSyncWithPostgreSQL:

    def test_create_table(self, database, mock_postgres_connection):
        mock_conn, mock_cur = mock_postgres_connection

        with patch(
            "pyside_demo.db.database.psycopg2.connect", return_value=mock_conn
        ), patch.object(
            database, "is_online", return_value=True
        ), patch.object(
            database, "get_items", return_value=[]
        ):

            database.sync_with_postgresql("host", "db", "user", "pass")

        mock_cur.execute.assert_any_call(SQL_CREATE_TABLE)

    def test_check_for_conflicts(
        self, database, mock_postgres_connection, mock_item
    ):
        mock_conn, mock_cur = mock_postgres_connection
        mock_cur.fetchone.return_value = (0,)  # Simulate no conflict

        with patch(
            "pyside_demo.db.database.psycopg2.connect", return_value=mock_conn
        ), patch.object(
            database, "is_online", return_value=True
        ), patch.object(
            database, "get_items", return_value=[mock_item]
        ):

            database.sync_with_postgresql("host", "db", "user", "pass")

        mock_cur.execute.assert_any_call(
            SQL_CHECK_FOR_CONFLICTS, (mock_item.id,)
        )

    def test_update_or_insert_item(
        self, database, mock_postgres_connection, mock_item
    ):
        mock_conn, mock_cur = mock_postgres_connection
        mock_cur.fetchone.return_value = (0,)  # Simulate no conflict

        with patch(
            "pyside_demo.db.database.psycopg2.connect", return_value=mock_conn
        ), patch.object(
            database, "is_online", return_value=True
        ), patch.object(
            database, "get_items", return_value=[mock_item]
        ):

            database.sync_with_postgresql("host", "db", "user", "pass")

        expected_params = (
            mock_item.id,
            mock_item.name,
            mock_item.description,
            mock_item.created_at,
            mock_item.updated_at,
            mock_item.version,
            "synced",
        )
        mock_cur.execute.assert_any_call(
            SQL_UPDATE_OR_INSERT_ITEM, expected_params
        )

    def test_fetch_items_from_postgresql(
        self, database, mock_postgres_connection
    ):
        mock_conn, mock_cur = mock_postgres_connection
        mock_cur.fetchall.return_value = []  # Simulate no items in PostgreSQL

        with patch(
            "pyside_demo.db.database.psycopg2.connect", return_value=mock_conn
        ), patch.object(
            database, "is_online", return_value=True
        ), patch.object(
            database, "get_items", return_value=[]
        ):

            database.sync_with_postgresql("host", "db", "user", "pass")

        mock_cur.execute.assert_any_call(SQL_FETCH_ITEMS)

    def test_commit_changes(self, database, mock_postgres_connection):
        mock_conn, mock_cur = mock_postgres_connection

        with patch(
            "pyside_demo.db.database.psycopg2.connect", return_value=mock_conn
        ), patch.object(
            database, "is_online", return_value=True
        ), patch.object(
            database, "get_items", return_value=[]
        ), patch.object(
            database, "Session"
        ) as mock_session_class:

            mock_session = Mock()
            mock_session_class.return_value = mock_session

            database.sync_with_postgresql("host", "db", "user", "pass")

        mock_conn.commit.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_close_connections(self, database, mock_postgres_connection):
        mock_conn, mock_cur = mock_postgres_connection

        with patch(
            "pyside_demo.db.database.psycopg2.connect", return_value=mock_conn
        ), patch.object(
            database, "is_online", return_value=True
        ), patch.object(
            database, "get_items", return_value=[]
        ):

            database.sync_with_postgresql("host", "db", "user", "pass")

        mock_cur.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_sync_offline(self, database):
        with patch.object(database, "is_online", return_value=False), patch(
            "pyside_demo.db.database.psycopg2.connect"
        ) as mock_connect:

            database.sync_with_postgresql("host", "db", "user", "pass")

        mock_connect.assert_not_called()
