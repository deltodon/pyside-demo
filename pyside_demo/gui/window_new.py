from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from pyside_demo.gui.home import HomeDashboard
from pyside_demo.gui.settings import SettingsWidget
from pyside_demo.gui.sidebar import SideBar
from pyside_demo.resources import rc_resources  # noqa: F401


class NewMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 App with Collapsible Sidebar")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QMenuBar {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMenuBar::item {
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #1E1E1E;
            }
            QMenu {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #505050;
            }
            QMenu::item:selected {
                background-color: #3E3E42;
            }
        """
        )

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = SideBar()
        sidebar_button_functions = [
            ("Home", self.show_home),
            ("New File", self.new_file),
            ("Open File", self.open_file),
            ("Search", self.search_files),
            ("Full Screen", self.toggle_full_screen),
            ("Settings", self.show_settings),
        ]

        for label, func in sidebar_button_functions:
            self.sidebar.on_click(label, func)

        # Create content area
        self.content_area = QStackedWidget()

        # Create home dashboard
        self.home_dashboard = HomeDashboard()
        self.content_area.addWidget(self.home_dashboard)

        # Create settings widget
        self.settings_widget = SettingsWidget()
        self.content_area.addWidget(self.settings_widget)

        # Add sidebar and content area to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)

        # Set central widget
        self.setCentralWidget(main_widget)

    def show_home(self):
        self.content_area.setCurrentWidget(self.home_dashboard)

    def show_settings(self):
        self.content_area.setCurrentWidget(self.settings_widget)

    def new_file(self):
        print("New File")

    def open_file(self):
        print("Open File")

    def search_files(self):
        print("Search")

    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
