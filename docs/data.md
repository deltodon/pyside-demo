# Data

## Synchronization Process

The synchronization process follows these steps:

1. Check for internet connectivity
2. Upload local changes to the PostgreSQL database
3. Download changes from the PostgreSQL database
4. Detect and resolve conflicts
5. Update local items' sync status

## Conflict Resolution

When a conflict is detected during synchronization:

1. The item's sync status is set to "conflict"
2. During the next sync attempt, a dialog appears for each conflicted item
3. The user can choose to keep the local version or use the remote version
4. The chosen version is then marked for synchronization in the next sync attempt

## Data Model

Items have the following properties:

* id: Unique identifier (UUID)
* name: Item name
* description: Item description
* created_at: Timestamp of creation
* updated_at: Timestamp of last update
* version: Integer representing the revision number
* sync_status: Current synchronization status (synced, modified, deleted, or conflict)
