from PySide6.QtWidgets import QMenuBar

from ..main_widget.object_explorer import ObjectExplorer
from ..main_widget.object_viewer import ObjectViewer
from .file_menu import FileMenu
from .edit_menu import EditMenu
from .help_menu import HelpMenu


class MenuBar(
    QMenuBar,
):

    object_explorer: ObjectExplorer
    object_viewer: ObjectViewer

    def __init__(
        self,
        parent,
        object_explorer: ObjectExplorer,
        object_viewer: ObjectViewer,
    ):

        QMenuBar.__init__(
            self,
            parent=parent,
        )

        self.object_explorer = object_explorer
        self.object_viewer = object_viewer

        self.addMenu(
            FileMenu(
                parent=self,
                object_explorer=object_explorer,
                object_viewer=object_viewer,
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
