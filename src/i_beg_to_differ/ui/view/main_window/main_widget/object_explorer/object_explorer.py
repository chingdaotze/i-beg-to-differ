from PySide6.QtWidgets import QTreeView

from .....model import Model


class ObjectExplorer(
    QTreeView,
):

    model: Model

    def __init__(
        self,
        parent,
    ):

        QTreeView.__init__(
            self,
            parent=parent,
        )

        self.model = Model()

        self.setModel(
            self.model,
        )
