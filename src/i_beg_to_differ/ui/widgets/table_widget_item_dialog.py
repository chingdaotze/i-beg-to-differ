"""
Contains definition of the TableWidgetItemDialog class.
"""

from abc import abstractmethod

from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt


class TableWidgetItemDialog(
    QTableWidgetItem,
):
    """
    Abstract class that represents an item in a table that products
    a dialog.
    """

    def __init__(
        self,
    ):

        QTableWidgetItem.__init__(
            self,
        )

        self.setFlags(
            Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable,
        )

        self.set_text()

    def set_text(
        self,
    ) -> None:
        """
        Sets the text representation of this object.
        """

        self.setText(
            self.get_text(),
        )

    @abstractmethod
    def get_text(
        self,
    ) -> str:
        """
        Text representation of this object.
        """

    @abstractmethod
    def open_dialog(
        self,
    ) -> None:
        """
        Abstract method that opens a dialog.
        """
