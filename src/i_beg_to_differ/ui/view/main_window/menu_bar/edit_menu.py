from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QKeySequence


class EditMenu(
    QMenu,
):

    def __init__(
        self,
        parent,
    ):

        QMenu.__init__(
            self,
            title='&Edit',
            parent=parent,
        )

        self.addAction(
            'Copy',
            QKeySequence.StandardKey.Copy,
        )

        self.addAction(
            'Cut',
            QKeySequence.StandardKey.Cut,
        )

        self.addAction(
            'Delete',
            QKeySequence.StandardKey.Delete,
        )

        self.addSeparator()

        self.addAction(
            'Paste',
            QKeySequence.StandardKey.Paste,
        )

        self.addSeparator()

        self.addAction(
            'Undo',
            QKeySequence.StandardKey.Undo,
        )
