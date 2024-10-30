from PySide6.QtWidgets import QTabWidget


class ObjectViewer(
    QTabWidget,
):

    def __init__(
        self,
        parent,
    ):

        QTabWidget.__init__(
            self,
            parent=parent,
        )

        self.setTabsClosable(
            True,
        )
