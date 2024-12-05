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

    MIN_WIDTH: ClassVar[int | None] = None
    MIN_HEIGHT: ClassVar[int | None] = None

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
        if self.MIN_WIDTH is not None and self.MIN_HEIGHT is not None:
            self.resize(
                self.MIN_WIDTH,
                self.MIN_HEIGHT,
            )

        if self.MIN_WIDTH is not None:
            self.setMinimumWidth(
                self.MIN_WIDTH,
            )

        if self.MIN_HEIGHT is not None:
            self.setMinimumHeight(
                self.MIN_HEIGHT,
            )

        # Layout
        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )
