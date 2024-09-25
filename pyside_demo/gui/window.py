from PySide6 import QtGui
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from pyside_demo.gui.data import DataWidget
from pyside_demo.gui.graph import GraphWidget
from pyside_demo.gui.home import HomeWidget
from pyside_demo.gui.map import MapWidget
from pyside_demo.gui.settings import SettingsWidget
from pyside_demo.gui.sidebar import SideBar
from pyside_demo.gui.table import TableWidget
from pyside_demo.gui.top_menu import create_menu_bar
from pyside_demo.model.table import TableModel
from pyside_demo.resources import rc_resources  # noqa: F401
from pyside_demo.resources.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setWindowTitle("PySide Demo")
        icon = QtGui.QIcon(":/icons/deltodon-logo.png")
        self.setWindowIcon(icon)

        self.setWindowTitle("PySide Demo")
        self.setGeometry(100, 100, 800, 600)
        create_menu_bar(self)

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = SideBar()
        self.sidebar.setObjectName("sidebar")
        sidebar_button_functions = [
            ("Home", self.show_home),
            ("Data", self.show_data),
            ("Table", self.show_table),
            ("Map", self.show_map),
            ("Graph", self.show_graph),
            # ("New File", self.new_file),
            # ("Open File", self.open_file),
            # ("Search", self.search_files),
            ("Full Screen", self.toggle_full_screen),
            ("Settings", self.show_settings),
        ]

        for label, func in sidebar_button_functions:
            self.sidebar.on_click(label, func)

        # Create table model
        self.table_model = TableModel()

        # Create content area
        self.content_area = QStackedWidget()

        # Create home widget
        self.home_dashboard = HomeWidget()
        self.content_area.addWidget(self.home_dashboard)

        # Create data widget
        self.data_widget = DataWidget(self.table_model)
        self.content_area.addWidget(self.data_widget)

        # Create table widget
        self.table_widget = TableWidget(self.table_model)
        self.content_area.addWidget(self.table_widget)

        # Create map widget
        self.map_widget = MapWidget()
        self.content_area.addWidget(self.map_widget)

        # Create graph widget
        self.graph_widget = GraphWidget()
        self.content_area.addWidget(self.graph_widget)

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

    def show_data(self):
        self.content_area.setCurrentWidget(self.data_widget)

    def show_table(self):
        self.content_area.setCurrentWidget(self.table_widget)

    def show_map(self):
        self.content_area.setCurrentWidget(self.map_widget)

    def show_graph(self):
        self.content_area.setCurrentWidget(self.graph_widget)

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
