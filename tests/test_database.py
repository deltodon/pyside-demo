from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

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
    return MagicMock(spec=Session)


@pytest.fixture
@patch("pyside_demo.db.database.sessionmaker")
@patch("pyside_demo.db.database.Base.metadata.create_all")
@patch("pyside_demo.db.database.create_engine")
def database(mock_create_engine, mock_create_all, mock_sessionmaker):
    return Database()


@pytest.fixture
def mock_postgres_connection():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur
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


@patch("pyside_demo.db.database.psycopg2.connect")
@patch.object(Database, "is_online", return_value=True)
@patch.object(Database, "get_items", return_value=[])
def test_create_table(
    mock_get_items,
    mock_is_online,
    mock_connect,
    database,
    mock_postgres_connection,
):
    mock_conn, mock_cur = mock_postgres_connection
    mock_connect.return_value = mock_conn

    database.sync_with_postgresql()

    mock_cur.execute.assert_any_call(SQL_CREATE_TABLE)


@patch("pyside_demo.db.database.psycopg2.connect")
@patch.object(Database, "is_online", return_value=True)
def test_check_for_conflicts(
    mock_is_online, mock_connect, database, mock_postgres_connection, mock_item
):
    mock_conn, mock_cur = mock_postgres_connection
    mock_connect.return_value = mock_conn
    mock_cur.fetchone.return_value = (0,)  # Simulate no conflict

    with patch.object(database, "get_items", return_value=[mock_item]):
        database.sync_with_postgresql()

    mock_cur.execute.assert_any_call(SQL_CHECK_FOR_CONFLICTS, (mock_item.id,))


@patch("pyside_demo.db.database.psycopg2.connect")
@patch.object(Database, "is_online", return_value=True)
def test_update_or_insert_item(
    mock_is_online, mock_connect, database, mock_postgres_connection, mock_item
):
    mock_conn, mock_cur = mock_postgres_connection
    mock_connect.return_value = mock_conn
    mock_cur.fetchone.return_value = (0,)  # Simulate no conflict

    with patch.object(database, "get_items", return_value=[mock_item]):
        database.sync_with_postgresql()

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


@patch("pyside_demo.db.database.psycopg2.connect")
@patch.object(Database, "is_online", return_value=True)
@patch.object(Database, "get_items", return_value=[])
def test_fetch_items_from_postgresql(
    mock_get_items,
    mock_is_online,
    mock_connect,
    database,
    mock_postgres_connection,
):
    mock_conn, mock_cur = mock_postgres_connection
    mock_connect.return_value = mock_conn
    mock_cur.fetchall.return_value = []  # Simulate no items in PostgreSQL

    database.sync_with_postgresql()

    mock_cur.execute.assert_any_call(SQL_FETCH_ITEMS)


@patch("pyside_demo.db.database.psycopg2.connect")
@patch.object(Database, "is_online", return_value=True)
@patch.object(Database, "get_items", return_value=[])
def test_context_manager_usage(
    mock_get_items,
    mock_is_online,
    mock_connect,
    database,
    mock_postgres_connection,
):
    mock_conn, mock_cur = mock_postgres_connection
    mock_connect.return_value = mock_conn

    database.sync_with_postgresql()

    # Check that the connection's context manager was used
    mock_conn.__enter__.assert_called_once()
    mock_conn.__exit__.assert_called_once()

    # Check that the cursor's context manager was used
    mock_conn.cursor.return_value.__enter__.assert_called_once()
    mock_conn.cursor.return_value.__exit__.assert_called_once()


@patch.object(Database, "is_online", return_value=False)
@patch("pyside_demo.db.database.psycopg2.connect")
def test_sync_offline(mock_connect, mock_is_online, database):
    database.sync_with_postgresql()

    mock_connect.assert_not_called()


def test_add_item(database, mock_session):
    with patch.object(database, "Session", return_value=mock_session):
        database.add_item("New Item", "New Description")

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()

    added_item = mock_session.add.call_args[0][0]
    assert isinstance(added_item, Item)
    assert added_item.name == "New Item"
    assert added_item.description == "New Description"


def test_update_item(database, mock_session, mock_item):
    with patch.object(database, "Session", return_value=mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = (  # noqa: E501
            mock_item
        )
        database.update_item("test_id", "Updated Item", "Updated Description")

    assert mock_item.name == "Updated Item"
    assert mock_item.description == "Updated Description"
    assert mock_item.version == 2
    assert mock_item.sync_status == SyncStatus.MODIFIED
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


def test_set_conflict(database, mock_session, mock_item):
    with patch.object(database, "Session", return_value=mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = (  # noqa: E501
            mock_item
        )
        database.set_conflict("test_id")

    assert mock_item.sync_status == SyncStatus.CONFLICT
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


def test_delete_item(database, mock_session, mock_item):
    with patch.object(database, "Session", return_value=mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = (  # noqa: E501
            mock_item
        )
        database.delete_item("test_id")

    assert mock_item.sync_status == SyncStatus.DELETED
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


def test_get_items(database, mock_session):
    mock_items = [Mock(spec=Item), Mock(spec=Item)]
    with patch.object(database, "Session", return_value=mock_session):
        mock_session.query.return_value.filter.return_value.all.return_value = (  # noqa: E501
            mock_items
        )
        result = database.get_items()

    assert result == mock_items
    mock_session.close.assert_called_once()


@pytest.mark.parametrize(
    "resolution_choice, expected_status",
    [
        ("local", SyncStatus.MODIFIED),
        (
            "remote",
            SyncStatus.CONFLICT,
        ),  # No change for 'remote' as it's not fully implemented
    ],
)
def test_resolve_conflict(
    database, mock_session, mock_item, resolution_choice, expected_status
):
    with patch.object(database, "Session", return_value=mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = (  # noqa: E501
            mock_item
        )
        mock_item.sync_status = SyncStatus.CONFLICT
        database.resolve_conflict("test_id", resolution_choice)

    assert mock_item.sync_status == expected_status
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


@patch("pyside_demo.db.database.psycopg2.connect")
@patch.object(Database, "is_online", return_value=True)
def test_sync_remote_to_local(
    mock_is_online, mock_connect, database, mock_postgres_connection
):
    mock_conn, mock_cur = mock_postgres_connection
    mock_connect.return_value = mock_conn

    # Mock remote items
    remote_items = [
        (
            "remote_id",
            "Remote Item",
            "Remote Description",
            datetime.now(),
            datetime.now(),
            1,
        )
    ]
    mock_cur.fetchall.return_value = remote_items

    with patch.object(database, "Session") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter_by.return_value.first.return_value = (  # noqa: E501
            None  # Item not in local DB
        )

        database.sync_with_postgresql()

    mock_session.add.assert_called_once()
    added_item = mock_session.add.call_args[0][0]
    assert isinstance(added_item, Item)
    assert added_item.id == "remote_id"
    assert added_item.name == "Remote Item"
    assert added_item.description == "Remote Description"
    assert added_item.sync_status == SyncStatus.SYNCED

    mock_session.commit.assert_called_once()
