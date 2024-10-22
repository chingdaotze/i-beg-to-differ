from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QKeySequence


class FileMenu(
    QMenu,
):

    def __init__(
        self,
        parent,
    ):

        QMenu.__init__(
            self,
            title='&File',
            parent=parent,
        )

        self.addAction(
            'New',
            QKeySequence.StandardKey.New,
        )

        self.addAction(
            'Open',
            QKeySequence.StandardKey.Open,
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
