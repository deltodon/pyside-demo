SQL_CREATE_TABLE: str = """
CREATE TABLE IF NOT EXISTS items (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    version INTEGER,
    sync_status VARCHAR(20)
)
"""

SQL_UPDATE_OR_INSERT_ITEM: str = """
INSERT INTO items (id, name, description, created_at,
                   updated_at, version, sync_status)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = EXCLUDED.updated_at,
    version = EXCLUDED.version,
    sync_status = EXCLUDED.sync_status
"""

SQL_FETCH_ITEMS: str = """
SELECT id,
       name,
       description,
       created_at,
       updated_at,
       version
FROM items
"""

SQL_CHECK_FOR_CONFLICTS: str = """
SELECT version FROM items WHERE id = %s
"""
