from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QKeySequence


class HelpMenu(
    QMenu,
):

    def __init__(
        self,
        parent,
    ):

        QMenu.__init__(
            self,
            title='&Help',
            parent=parent,
        )

        self.addAction(
            'Online Help',
            QKeySequence.StandardKey.HelpContents,
        )

        self.addAction(
            'About',
        )
