from typing import Callable, Dict, List, Tuple

import qtawesome as qta
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSize
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout


class SidebarButton(QPushButton):
    def __init__(self, label: str, icon: str):
        super().__init__()
        self.setIcon(qta.icon(icon, color="white"))
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(50, 50)

        self.label = label
        # Start with no label
        self.setText("")

        self.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #3E3E42;
            }
        """
        )

    def set_expanded(self, expanded):
        if expanded:
            self.setText(self.label)
            self.setFixedSize(200, 50)
        else:
            self.setText("")
            self.setFixedSize(50, 50)


class SideBar(QFrame):
    def __init__(
        self,
    ):
        super().__init__()
        self.sidebar_expanded = False
        self.setStyleSheet("background-color: #252526;")
        self.setFixedWidth(50)
        self.sidebar_layout = QVBoxLayout(self)
        self.sidebar_layout.setContentsMargins(0, 10, 0, 0)
        self.sidebar_layout.setSpacing(10)

        # Add buttons to the sidebar
        self.create_sidebar_buttons()
        self.on_click("Toggle Sidebar", self.toggle_sidebar)

    def create_sidebar_buttons(self):
        buttons_params: List[Tuple[str, str]] = [
            ("Toggle Sidebar", "fa5s.bars"),
            ("Home", "fa5s.home"),
            ("New File", "fa5s.file"),
            ("Open File", "fa5s.folder-open"),
            ("Search", "fa5s.search"),
            ("Full Screen", "fa5s.expand"),
            ("Settings", "fa5s.cog"),
        ]

        self.buttons: Dict[str, SidebarButton] = {}
        for label, icon in buttons_params:
            button = SidebarButton(label, icon)
            self.buttons[label] = button
            self.sidebar_layout.addWidget(button)

        # Add stretch at the end to push buttons to the top
        self.sidebar_layout.addStretch()

    def toggle_sidebar(self):
        width = 200 if not self.sidebar_expanded else 50
        self.sidebar_expanded = not self.sidebar_expanded

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

        for button in self.buttons.values():
            button.set_expanded(self.sidebar_expanded)

    def on_click(self, button_label: str, func: Callable):
        self.buttons[button_label].clicked.connect(func)
