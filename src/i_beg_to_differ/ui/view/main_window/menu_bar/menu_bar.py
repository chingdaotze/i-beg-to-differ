from PySide6.QtWidgets import QMenuBar

from .file_menu import FileMenu
from .edit_menu import EditMenu
from .help_menu import HelpMenu


class MenuBar(
    QMenuBar,
):

    def __init__(
        self,
        parent,
    ):

        QMenuBar.__init__(
            self,
            parent=parent,
        )

        self.addMenu(
            FileMenu(
                parent=self,
            ),
        )

        self.addMenu(
            EditMenu(
                parent=self,
            ),
        )

        self.addMenu(
            HelpMenu(
                parent=self,
            ),
        )
