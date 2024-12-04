from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)


class Widget(
    QWidget,
):
    """
    Basic QWidget that provides a QGridLayout.
    """

    layout: QGridLayout

    def __init__(
        self,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent,
        )

        self.layout = QGridLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.setLayout(
            self.layout,
        )
