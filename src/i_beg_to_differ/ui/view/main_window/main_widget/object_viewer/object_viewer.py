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

        self.tabCloseRequested.connect(
            self.close_tab,
        )

    def close_tab(
        self,
        index,
    ) -> None:

        self.removeTab(
            index,
        )
