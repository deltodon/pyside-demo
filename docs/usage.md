# Usage

This guide provides an overview of how to use the PySide Demo application.

## Starting the Application

1. After installation, you can start the application by running:

   ```bash
   python -m pyside_demo
   ```

   or if you juse Poetry

   ```bash
   poetry run python pyside_demo
   ```

2. Use the GUI to add, edit, and view items:
   * Enter item details in the left panel and click "Add Item" or "Update Item"
   * View and select items from the list in the right panel

3. Synchronize with PostgreSQL:
   * Click the "Sync with PostgreSQL" button to initiate synchronization
   * If conflicts are detected, a dialog will appear for each conflict, allowing you to choose between the local and remote versions

## Main Features

1. Offline Mode
   * The application works without an internet connection
   * Data is stored locally

2. Synchronization
   * When online, the app syncs local data with the PostgreSQL database
   * Sync status is displayed in the UI

3. GUI Interface
   * [Describe main windows/screens]
   * [Explain key UI elements and their functions]

4. Data Management
   * [Explain how to add/edit/delete data]
   * [Describe any data visualization features]

## Tips and Tricks

* [Add any useful tips for users]
* [Describe keyboard shortcuts if applicable]

## Troubleshooting

* [List common issues and their solutions]
* [Provide guidance on where to find logs or how to report bugs]

For more detailed information on specific features, please refer to the respective sections in the documentation.
