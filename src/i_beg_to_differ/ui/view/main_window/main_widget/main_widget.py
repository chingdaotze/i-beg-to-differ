from PySide6.QtWidgets import QWidget, QSplitter
from PySide6.QtCore import Qt

from .object_explorer import ObjectExplorer
from .object_viewer import ObjectViewer


class MainWidget(
    QSplitter,
):

    object_explorer: ObjectExplorer
    object_viewer: ObjectViewer

    def __init__(
        self,
        parent,
    ):

        QSplitter.__init__(
            self,
            Qt.Orientation.Horizontal,
            parent=parent,
        )

        self.object_viewer = ObjectViewer(
            parent=self,
        )

        self.object_explorer = ObjectExplorer(
            parent=self,
            object_viewer=self.object_viewer,
        )

        self.addWidget(
            self.object_explorer,
        )

        self.addWidget(
            self.object_viewer,
        )

        self.setSizes(
            [
                200,
                600,
            ],
        )
