from PySide6.QtWidgets import (
    QMenuBar,
    QStatusBar,
)

from ..main_widget.object_explorer import ObjectExplorer
from ..main_widget.object_viewer import ObjectViewer
from .file_menu import FileMenu
from .edit_menu import EditMenu
from .help_menu import HelpMenu


class MenuBar(
    QMenuBar,
):

    file_menu: FileMenu
    edit_menu: EditMenu
    help_menu: HelpMenu

    def __init__(
        self,
        parent,
        object_explorer: ObjectExplorer,
        status_bar: QStatusBar,
        object_viewer: ObjectViewer,
    ):

        QMenuBar.__init__(
            self,
            parent=parent,
        )

        self.file_menu = FileMenu(
            parent=self,
            object_explorer=object_explorer,
            status_bar=status_bar,
            object_viewer=object_viewer,
        )

        self.addMenu(
            self.file_menu,
        )

        self.edit_menu = EditMenu(
            parent=self,
        )

        self.addMenu(
            self.edit_menu,
        )

        self.help_menu = HelpMenu(
            parent=self,
        )

        self.addMenu(
            self.help_menu,
        )
