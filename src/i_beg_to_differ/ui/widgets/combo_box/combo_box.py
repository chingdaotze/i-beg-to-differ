from abc import abstractmethod
from typing import List

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import (
    QComboBox,
    QCompleter,
    QWidget,
)

from ..text_widget import TextWidget


class ComboBox(
    TextWidget,
    QComboBox,
):
    """
    Abstract QComboBox class.
    """

    def __init__(
        self,
        value: str | None = None,
        parent: QWidget | None = None,
    ):

        QComboBox.__init__(
            self,
            parent,
        )

        self.setEditable(
            True,
        )

        self.setInsertPolicy(
            QComboBox.InsertPolicy.NoInsert,
        )

        TextWidget.__init__(
            self=self,
            value=value,
        )

    @property
    @abstractmethod
    def options(
        self,
    ) -> List[str]:
        """
        Returns a list of options for the combo box.
        """

    @property
    def text_changed(
        self,
    ) -> SignalInstance:

        return self.currentTextChanged

    def get_text(
        self,
    ) -> str:

        return self.currentText()

    def set_text(
        self,
        value: str,
    ) -> None:

        self.setCurrentText(
            value,
        )

    def showPopup(
        self,
    ) -> None:

        self.clear()

        self.addItems(
            self.options,
        )

        self.setCompleter(
            QCompleter(
                self.options,
                self,
            ),
        )

        QComboBox.showPopup(
            self,
        )
