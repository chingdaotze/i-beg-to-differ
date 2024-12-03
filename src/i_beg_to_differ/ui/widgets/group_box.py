from PySide6.QtWidgets import (
    QGroupBox,
    QGridLayout,
)


class GroupBox(
    QGroupBox,
):
    """
    Basic QGroupBox that provides a QGridLayout and title.
    """

    layout: QGridLayout

    def __init__(
        self,
        title: str | None = None,
    ):

        QGroupBox.__init__(
            self,
        )

        if title is not None:
            self.setTitle(
                title,
            )

        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )
