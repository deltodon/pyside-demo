# PySide Demo

* [Overview](#overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Synchronization Process](#synchronization-process)
* [Conflict Resolution](#conflict-resolution)
* [Data Model](#data-model)
* [Contributing](#contributing)

## Overview

This application is a PySide6-based GUI that demonstrates an offline-first approach with PostgreSQL synchronization capabilities.
It allows users to manage items locally and synchronize them with a remote PostgreSQL database when an internet connection is available.

## Features

* Add, edit, and view items in a local SQLite database
* Offline-first functionality: work without an internet connection
* Synchronize local data with a remote PostgreSQL database
* Sophisticated conflict resolution mechanism
* User-friendly GUI built with PySide6

## Prerequisites

* Python 3.9 or higher
* Poetry (for dependency management)
* PostgreSQL server (for remote synchronization)

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:jiriklic/pyside-demo.git
   cd pyside-demo
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install 
   ```

3. Install pre-commit hooks (optional):

   ```bash
   poetry run pre-commit install
   ```

## Configuration

Before running the application, you need to configure the PostgreSQL connection details:

1. Open `gui.py`
2. Locate the `sync_with_postgresql` method in the `MainWindow` class
3. Update the following variables with your PostgreSQL server details:

```python
host = "your_host"
database = "your_database"
user = "your_username"
password = "your_password"
```

## Usage

1. Build the project:

   ```bash
   poetry run pyside6-project build pyside_demo
   ```

2. Run the application:

   ```bash
   poetry run python pyside_demo
   ```

3. Use the GUI to add, edit, and view items:
   * Enter item details in the left panel and click "Add Item" or "Update Item"
   * View and select items from the list in the right panel

4. Synchronize with PostgreSQL:
   * Click the "Sync with PostgreSQL" button to initiate synchronization
   * If conflicts are detected, a dialog will appear for each conflict, allowing you to choose between the local and remote versions

5. Run unit tests:

   ```bash
   poetry run python -m pytest -v
   ```

6. Run mypy test:

   ```bash
   poetry run mypy .
   ```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
