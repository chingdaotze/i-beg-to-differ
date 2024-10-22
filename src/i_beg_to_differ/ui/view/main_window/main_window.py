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
        self.setMenuBar(
            MenuBar(
                parent=self,
            )
        )

        self.setStatusBar(
            StatusBar(
                parent=self,
            )
        )

        # Widgets
        self.setCentralWidget(
            MainWidget(
                parent=self,
            ),
        )
