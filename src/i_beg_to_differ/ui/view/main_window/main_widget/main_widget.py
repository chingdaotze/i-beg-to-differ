from PySide6.QtWidgets import (
    QSplitter,
    QStatusBar,
    QWidget,
)
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
        status_bar: QStatusBar,
        parent: QWidget | None = None,
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
            status_bar=status_bar,
            object_viewer=self.object_viewer,
            parent=self,
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
