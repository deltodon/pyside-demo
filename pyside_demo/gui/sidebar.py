from typing import Callable, Dict, List, Tuple

import qtawesome as qta
from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QPropertyAnimation,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import QEnterEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

SIDEBAR_WIDTH_EXPANDED: int = 200
SIDEBAR_WIDTH_COLLAPSED: int = 50
BUTTON_HEIGHT: int = 50
ICON_SIZE: int = 20
ANIMATION_DURATION: int = 300


class SidebarButton(QWidget):
    """
    A custom sidebar button widget with an icon and label.

    This widget creates a button with an icon and label for use in a sidebar.
    It can be expanded or collapsed, showing or hiding the label text.

    Attributes:
        clicked (Signal): Signal emitted when the button is clicked.
    """

    clicked = Signal()

    def __init__(self, label: str, icon: str):
        """
        Initialize the SidebarButton.

        Args:
            label (str): The text to display on the button.
            icon (str): The name of the icon to display on the button.
        """
        super().__init__()
        self.label_text = label

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(SIDEBAR_WIDTH_COLLAPSED, BUTTON_HEIGHT)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setPixmap(
            qta.icon(icon, color="white").pixmap(QSize(ICON_SIZE, ICON_SIZE))
        )

        self.text_label = QLabel(label)
        # used in qss to set the spacing between icon and label
        self.text_label.setObjectName("text-label")
        # Initially hide the text
        self.text_label.hide()

        self.content_layout.addWidget(self.icon_label)
        self.content_layout.addWidget(self.text_label)
        self.content_layout.addStretch()

        self.main_layout.addWidget(self.content_widget)

        self.setFixedHeight(BUTTON_HEIGHT)
        self.setFixedWidth(
            SIDEBAR_WIDTH_COLLAPSED
        )  # Start with collapsed width
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

    def set_expanded(self, expanded):
        """
        Set the expanded state of the button.

        Args:
            expanded (bool): True to expand the button, False to collapse it.
        """
        if expanded:
            self.text_label.show()
            self.setFixedWidth(SIDEBAR_WIDTH_EXPANDED)
        else:
            self.text_label.hide()
            self.setFixedWidth(SIDEBAR_WIDTH_COLLAPSED)

    def enterEvent(self, event: QEnterEvent) -> None:
        """
        Handle the mouse enter event.

        Args:
            event (QEnterEvent): The enter event.
        """
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """
        Handle the mouse leave event.

        Args:
            event (QEvent): The leave event.
        """
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """
        Handle the mouse press event.

        Args:
            event (QMouseEvent): The mouse press event.
        """
        self.clicked.emit()


class SideBar(QFrame):
    def __init__(
        self,
    ):
        super().__init__()
        self.sidebar_expanded = False
        self.setFixedWidth(SIDEBAR_WIDTH_COLLAPSED)
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
            ("Data", "fa5s.database"),
            ("Table", "fa.table"),
            ("Map", "fa5s.map"),
            ("Graph", "fa5s.chart-line"),
            # ("New File", "fa5s.file"),
            # ("Open File", "fa5s.folder-open"),
            # ("Search", "fa5s.search"),
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
        width = (
            SIDEBAR_WIDTH_EXPANDED
            if not self.sidebar_expanded
            else SIDEBAR_WIDTH_COLLAPSED
        )
        self.sidebar_expanded = not self.sidebar_expanded

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(ANIMATION_DURATION)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()

        for button in self.buttons.values():
            button.set_expanded(self.sidebar_expanded)

    def on_click(self, button_label: str, func: Callable):
        self.buttons[button_label].clicked.connect(func)
