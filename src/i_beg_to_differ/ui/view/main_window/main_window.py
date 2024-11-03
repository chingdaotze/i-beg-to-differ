from typing import ClassVar

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QSize

from .menu_bar import MenuBar
from .status_bar import StatusBar
from .main_widget import MainWidget


class MainWindow(
    QMainWindow,
):

    MIN_SIZE: ClassVar[QSize] = QSize(
        800,
        600,
    )

    main_widget: MainWidget
    menu_bar: MenuBar
    status_bar: StatusBar

    def __init__(
        self,
    ):

        QMainWindow.__init__(
            self,
        )

        # Window
        self.setWindowTitle(
            'I Beg to Differ!',
        )

        self.resize(
            self.MIN_SIZE,
        )

        self.setMinimumSize(
            self.MIN_SIZE,
        )

        # Bars
        self.main_widget = MainWidget(
            parent=self,
        )

        self.menu_bar = MenuBar(
            parent=self,
            object_explorer=self.main_widget.object_explorer,
            object_viewer=self.main_widget.object_viewer,
        )

        self.setMenuBar(
            self.menu_bar,
        )

        self.status_bar = StatusBar(
            parent=self,
        )

        self.setStatusBar(
            self.status_bar,
        )

        # Widgets
        self.setCentralWidget(
            self.main_widget,
        )
