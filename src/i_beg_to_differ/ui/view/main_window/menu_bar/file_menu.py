from typing import NoReturn
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
            self.new,
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
            self.save,
        )

        self.addAction(
            'Save As',
            QKeySequence.StandardKey.SaveAs,
            self.save_as,
        )

        self.addSeparator()

        self.addAction(
            'Quit',
            QKeySequence.StandardKey.Quit,
            self.quit,
        )

    def new(
        self,
    ) -> None:

        model = Model(
            status_bar=self.status_bar,
            object_viewer=self.object_viewer,
        )

        self.object_explorer.setModel(
            model,
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

            self.status_bar.showMessage(
                f'Loading *.ib2d file: {path} ...',
            )

            self.status_bar.repaint()

            model = Model.load(
                status_bar=self.status_bar,
                object_viewer=self.object_viewer,
                path=path,
            )

            self.object_explorer.setModel(
                model,
            )

            self.status_bar.showMessage(
                f'Loaded *.ib2d file: {path}',
            )

    def save(
        self,
    ) -> None:

        model: Model = self.object_explorer.model()

        if model.ib2d_file.path is not None:
            path = model.ib2d_file.path

            self.status_bar.showMessage(
                f'Saving *.ib2d file: {path} ...',
            )

            self.status_bar.repaint()

            model.ib2d_file.save(
                path=path,
            )

            self.status_bar.showMessage(
                f'Saved *.ib2d file: {path}',
            )

        else:
            self.save_as()

    def save_as(
        self,
        path: str | None = None,
    ) -> None:

        if path is None:
            path, _ = QFileDialog.getSaveFileName(
                self,
                caption='Save *.ib2d File',
                filter='ib2d Files (*.ib2d)',
            )

        if path:
            self.status_bar.showMessage(
                f'Saving *.ib2d file: {path} ...',
            )

            self.status_bar.repaint()

            model: Model = self.object_explorer.model()
            model.ib2d_file.save(
                path=path,
            )

            self.status_bar.showMessage(
                f'Saved *.ib2d file: {path}',
            )

    @staticmethod
    def quit() -> NoReturn:

        exit(
            0,
        )
