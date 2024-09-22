from PySide6.QtWidgets import QMainWindow


def create_menu_bar(window: QMainWindow):
    menu_bar = window.menuBar()

    # File menu
    file_menu = menu_bar.addMenu("File")
    file_menu.addAction("New File")
    file_menu.addAction("Open File")
    file_menu.addAction("Save")
    file_menu.addAction("Exit")

    # Edit menu
    edit_menu = menu_bar.addMenu("Edit")
    edit_menu.addAction("Undo")
    edit_menu.addAction("Redo")
    edit_menu.addAction("Cut")
    edit_menu.addAction("Copy")
    edit_menu.addAction("Paste")

    # Selection menu
    selection_menu = menu_bar.addMenu("Selection")
    selection_menu.addAction("Select All")
    selection_menu.addAction("Expand Selection")

    # View menu
    view_menu = menu_bar.addMenu("View")
    view_menu.addAction("Toggle Sidebar")
    view_menu.addAction("Toggle Panel")

    # Go menu
    go_menu = menu_bar.addMenu("Go")
    go_menu.addAction("Go to File")
    go_menu.addAction("Go to Symbol")

    # Run menu
    run_menu = menu_bar.addMenu("Run")
    run_menu.addAction("Start Debugging")
    run_menu.addAction("Run Without Debugging")

    # Terminal menu
    terminal_menu = menu_bar.addMenu("Terminal")
    terminal_menu.addAction("New Terminal")
    terminal_menu.addAction("Split Terminal")

    # Help menu
    help_menu = menu_bar.addMenu("Help")
    help_menu.addAction("Welcome")
    help_menu.addAction("Documentation")
    help_menu.addAction("About")
