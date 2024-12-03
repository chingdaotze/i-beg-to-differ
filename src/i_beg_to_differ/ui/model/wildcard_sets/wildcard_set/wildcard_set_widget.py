from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
)

from .....core.wildcards_sets.wildcard_set import WildcardSet
from ....widgets import TableWidget


class WildcardSetWidget(
    TableWidget,
):

    wildcard_set: WildcardSet

    def __init__(
        self,
        wildcard_set: WildcardSet,
        parent: QWidget | None = None,
    ):

        TableWidget.__init__(
            self,
            columns=[
                'Wildcard Name',
                'Wildcard Value',
            ],
            parent=parent,
        )

        # Build table
        self.wildcard_set = wildcard_set

        for key, value in self.wildcard_set.user_replacement_values.items():
            self.add_row()
            row = self.table.rowCount()

            key_widget = QTableWidgetItem(
                key,
            )

            value_widget = QTableWidgetItem(
                value,
            )

            self.table.setItem(
                row - 1,
                0,
                key_widget,
            )

            self.table.setItem(
                row - 1,
                1,
                value_widget,
            )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:

        key = self.table.item(
            row,
            0,
        )

        if isinstance(key, QTableWidgetItem):
            key = key.text()

        value = self.table.item(
            row,
            1,
        )

        if isinstance(value, QTableWidgetItem):
            value = value.text()

        self.wildcard_set.user_replacement_values[key] = value

    def delete_current_row(
        self,
    ) -> None:

        row = self.table.currentRow()

        key = self.table.item(
            row,
            0,
        )

        key = key.text()

        del self.wildcard_set.user_replacement_values[key]

        TableWidget.delete_current_row(
            self=self,
        )
