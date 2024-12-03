from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import (
    QLineEdit,
    QWidget,
)

from .text_widget import TextWidget


class LineEdit(
    TextWidget,
    QLineEdit,
):
    """
    QLineEdit with normalized string retrieval.
    """

    def __init__(
        self,
        value: str | None = None,
        parent: QWidget | None = None,
    ):

        QLineEdit.__init__(
            self,
            parent,
        )

        TextWidget.__init__(
            self=self,
            value=value,
        )

    @property
    def text_changed(
        self,
    ) -> SignalInstance:

        return self.textChanged

    def get_text(
        self,
    ) -> str:

        return self.text()

    def set_text(
        self,
        value: str,
    ) -> None:

        self.setText(
            value,
        )
