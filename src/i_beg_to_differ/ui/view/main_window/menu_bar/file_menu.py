from PySide6.QtWidgets import (
    QMenu,
    QStatusBar,
    QFileDialog,
)
from PySide6.QtGui import QKeySequence

from ..main_widget.object_explorer import ObjectExplorer
from ..main_widget.object_viewer import ObjectViewer
from ....model import Model


class FileMenu(
    QMenu,
):

    object_explorer: ObjectExplorer
    status_bar: QStatusBar
    object_viewer: ObjectViewer

    def __init__(
        self,
        parent,
        object_explorer: ObjectExplorer,
        status_bar: QStatusBar,
        object_viewer: ObjectViewer,
    ):

        QMenu.__init__(
            self,
            title='&File',
            parent=parent,
        )

        self.object_explorer = object_explorer
        self.status_bar = status_bar
        self.object_viewer = object_viewer

        self.addAction(
            'New',
            QKeySequence.StandardKey.New,
        )

        self.addAction(
            'Open',
            QKeySequence.StandardKey.Open,
            self.open,
        )

        self.addSeparator()

        self.addAction(
            'Save',
            QKeySequence.StandardKey.Save,
        )

        self.addAction(
            'Save As',
            QKeySequence.StandardKey.SaveAs,
        )

        self.addSeparator()

        self.addAction(
            'Quit',
            QKeySequence.StandardKey.Quit,
        )

    def open(
        self,
        path: str | None = None,
    ) -> None:

        if path is None:
            path, _ = QFileDialog.getOpenFileName(
                self,
                caption='Open *.ib2d File',
                filter='ib2d Files (*.ib2d)',
            )

        if path:
            model = Model.load(
                status_bar=self.status_bar,
                object_viewer=self.object_viewer,
                path=path,
            )

            self.object_explorer.setModel(
                model,
            )
