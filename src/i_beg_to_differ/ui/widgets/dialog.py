from typing import ClassVar

from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QWidget,
)


class Dialog(
    QDialog,
):

    layout: QGridLayout

    MIN_WIDTH: ClassVar[int]
    MIN_HEIGHT: ClassVar[int]

    def __init__(
        self,
        title: str | None = None,
        parent: QWidget | None = None,
    ):

        QDialog.__init__(
            self,
            parent,
        )

        # Window title
        if title is not None:
            self.setWindowTitle(
                title,
            )

        # Sizing
        self.resize(
            self.MIN_WIDTH,
            self.MIN_HEIGHT,
        )

        self.setMinimumWidth(
            self.MIN_WIDTH,
        )

        self.setMinimumHeight(
            self.MIN_HEIGHT,
        )

        # Layout
        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )
