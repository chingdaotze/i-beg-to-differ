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
        main_widget = MainWidget(
            parent=self,
        )

        self.setMenuBar(
            MenuBar(
                parent=self,
                object_explorer=main_widget.object_explorer,
                object_viewer=main_widget.object_viewer,
            )
        )

        self.setStatusBar(
            StatusBar(
                parent=self,
            )
        )

        # Widgets
        self.setCentralWidget(
            main_widget,
        )
