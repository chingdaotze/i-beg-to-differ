from PySide6.QtWidgets import QWidget, QSplitter
from PySide6.QtCore import Qt

from .object_explorer import ObjectExplorer
from .object_viewer import ObjectViewer


class MainWidget(
    QSplitter,
):

    def __init__(
        self,
        parent,
    ):

        QSplitter.__init__(
            self,
            Qt.Orientation.Horizontal,
            parent=parent,
        )

        self.addWidget(
            ObjectExplorer(
                parent=self,
            ),
        )

        self.addWidget(
            ObjectViewer(
                parent=self,
            ),
        )

        self.setSizes(
            [
                200,
                600,
            ],
        )
