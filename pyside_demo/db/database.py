import os
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Optional

import psycopg2
import requests
from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from pyside_demo.db.sql import (
    SQL_CHECK_FOR_CONFLICTS,
    SQL_CREATE_TABLE,
    SQL_DELETE_ITEM,
    SQL_FETCH_ITEMS,
    SQL_UPDATE_OR_INSERT_ITEM,
)


class Base(DeclarativeBase):
    """
    Base class for declarative SQLAlchemy models.

    This class serves as the base for all database models in the application.
    It inherits from SQLAlchemy's DeclarativeBase, providing the necessary
    functionality for declarative model definitions.
    """

    pass


SQLITE_FILE_NAME: str = "local.db"


class SyncStatus(str, PyEnum):
    SYNCED = "synced"
    MODIFIED = "modified"
    DELETED = "deleted"
    CONFLICT = "conflict"


class Item(Base):
    __tablename__ = "items"

    id: Any = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Any = Column(String)
    description: Any = Column(String)
    created_at: Any = Column(DateTime, default=datetime.utcnow)
    updated_at: Any = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    version: Any = Column(Integer, default=1)
    sync_status: Any = Column(
        SQLAlchemyEnum(SyncStatus), default=SyncStatus.MODIFIED
    )


class Database:
    def __init__(self):
        self.local_engine = create_engine(f"sqlite:///{SQLITE_FILE_NAME}")
        Base.metadata.create_all(self.local_engine)
        self.Session = sessionmaker(bind=self.local_engine)
        self.pg_host: Optional[str] = os.getenv("DB_HOST")
        self.pg_database: Optional[str] = os.getenv("DB_NAME")
        self.pg_user: Optional[str] = os.getenv("DB_USER")
        self.pg_password: Optional[str] = os.getenv("DB_PASSWORD")

    def add_item(self, name, description):
        session = self.Session()
        new_item = Item(name=name, description=description)
        session.add(new_item)
        session.commit()
        session.close()

    def update_item(self, item_id, name, description):
        session = self.Session()
        item = session.query(Item).filter_by(id=item_id).first()
        if item:
            item.name = name
            item.description = description
            item.version += 1
            item.sync_status = SyncStatus.MODIFIED
            session.commit()
        session.close()

    def set_conflict(self, item_id):
        session = self.Session()
        item = session.query(Item).filter_by(id=item_id).first()
        if item:
            item.sync_status = SyncStatus.CONFLICT
            session.commit()
        session.close()

    def delete_item(self, item_id):
        session = self.Session()
        item = session.query(Item).filter_by(id=item_id).first()
        if item:
            item.sync_status = SyncStatus.DELETED
            session.commit()
        session.close()

    def get_items(self):
        session = self.Session()
        items = (
            session.query(Item)
            .filter(Item.sync_status != SyncStatus.DELETED)
            .all()
        )
        session.close()
        return items

    def is_online(self):
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def sync_with_postgresql(self):
        if not self.is_online():
            print("Not online, can't sync with PostgreSQL")
            return

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(
                host=self.pg_host,
                database=self.pg_database,
                user=self.pg_user,
                password=self.pg_password,
            )
            cur = conn.cursor()

            # Create table if not exists
            cur.execute(SQL_CREATE_TABLE)

            # Get local items
            local_items = self.get_items()

            # Synchronize items
            for item in local_items:
                if item.sync_status == SyncStatus.MODIFIED:
                    # Check for conflicts
                    cur.execute(SQL_CHECK_FOR_CONFLICTS, (item.id,))
                    result = cur.fetchone()

                    if result and result[0] > item.version:
                        # Conflict detected
                        # item.sync_status = SyncStatus.CONFLICT
                        self.set_conflict(item.id)
                    else:
                        # Update or insert item
                        cur.execute(
                            SQL_UPDATE_OR_INSERT_ITEM,
                            (
                                item.id,
                                item.name,
                                item.description,
                                item.created_at,
                                item.updated_at,
                                item.version,
                                "synced",
                            ),
                        )
                        item.sync_status = SyncStatus.SYNCED

                elif item.sync_status == SyncStatus.DELETED:
                    # Delete item from PostgreSQL
                    cur.execute(
                        SQL_DELETE_ITEM,
                        (item.id,),
                    )

            # Fetch items from PostgreSQL that are not in local database
            cur.execute(SQL_FETCH_ITEMS)
            pg_items = cur.fetchall()

            session = self.Session()
            for pg_item in pg_items:
                local_item = (
                    session.query(Item).filter_by(id=pg_item[0]).first()
                )
                if not local_item:
                    new_item = Item(
                        id=pg_item[0],
                        name=pg_item[1],
                        description=pg_item[2],
                        created_at=pg_item[3],
                        updated_at=pg_item[4],
                        version=pg_item[5],
                        sync_status=SyncStatus.SYNCED,
                    )
                    session.add(new_item)

            session.commit()
            session.close()

            print("Sync with PostgreSQL completed successfully")

        except Exception as e:
            print(f"Error syncing with PostgreSQL: {e}")
            # Re-raise the exception to ensure
            # the test fails if an error occurs
            raise

        finally:
            if conn:
                if cur:
                    cur.close()
                conn.commit()
                conn.close()

    def resolve_conflict(self, item_id, resolution_choice):
        session = self.Session()
        item = session.query(Item).filter_by(id=item_id).first()
        if item and item.sync_status == SyncStatus.CONFLICT:
            if resolution_choice == "local":
                item.sync_status = SyncStatus.MODIFIED
            elif resolution_choice == "remote":
                # TODO: Fetch the latest version
                # from PostgreSQL and update local
                pass
            session.commit()
        session.close()
