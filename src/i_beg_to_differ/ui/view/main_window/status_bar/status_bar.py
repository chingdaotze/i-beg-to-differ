from PySide6.QtWidgets import QStatusBar


class StatusBar(
    QStatusBar,
):

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
