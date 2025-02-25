"""
Contains definition of the HelpMenu class.
"""

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QKeySequence


class HelpMenu(
    QMenu,
):
    """
    Main window help menu.
    """

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
