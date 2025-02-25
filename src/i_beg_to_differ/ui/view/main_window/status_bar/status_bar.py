"""
Contains definition of the StatusBar class.
"""

from PySide6.QtWidgets import QStatusBar


class StatusBar(
    QStatusBar,
):
    """
    Main window status bar.
    """

    def __init__(
        self,
        parent,
    ):

        QStatusBar.__init__(
            self,
            parent=parent,
        )

        self.showMessage(
            'Ready',
        )
