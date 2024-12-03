from typing import Dict

from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
)

from .....ui.widgets import TableWidget
from ....wildcards_sets.wildcard_field import WildcardField
from ....wildcards_sets import WildcardSets


class WildcardDictTableWidget(
    TableWidget,
):
    """
    Widget that creates a table of key-value pairs, with Wildcard value substitution in both
    keys and values.
    """

    values = Dict[WildcardField, WildcardField]
    wildcard_sets: WildcardSets

    def __init__(
        self,
        values: Dict[str, str] | None = None,
        wildcard_sets: WildcardSets | None = None,
        key_column: str = 'Parameter',
        value_column: str = 'Value',
        parent: QWidget | None = None,
    ):

        TableWidget.__init__(
            self=self,
            columns=[
                key_column,
                f'{key_column} Preview',
                value_column,
                f'{value_column} Preview',
            ],
            parent=parent,
        )

        self.wildcard_sets = wildcard_sets

        if values is None:
            values = {}

        self.values = {
            WildcardField(
                base_value=key,
                wildcard_sets=self.wildcard_sets,
            ): WildcardField(
                base_value=value,
                wildcard_sets=self.wildcard_sets,
            )
            for key, value in values.items()
        }

        for key, value in self.values.items():
            self.add_row()
            row = self.table.rowCount()

            table_widget_items = [
                QTableWidgetItem(
                    key.base_value,
                ),
                QTableWidgetItem(
                    str(key),
                ),
                QTableWidgetItem(
                    value.base_value,
                ),
                QTableWidgetItem(
                    str(value),
                ),
            ]

            for col, table_widget_item in enumerate(table_widget_items):
                self.table.setItem(
                    row - 1,
                    col,
                    table_widget_item,
                )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:

        # Key
        key = self.table.item(
            row,
            0,
        )

        key = WildcardField(
            base_value=key.text(),
            wildcard_sets=self.wildcard_sets,
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                str(key),
            ),
        )

        # Value
        value = self.table.item(
            row,
            2,
        )

        value = WildcardField(
            base_value=value.text(),
            wildcard_sets=self.wildcard_sets,
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem(
                str(value),
            ),
        )

        # Update dict
        self.values[key] = value

    def delete_current_row(
        self,
    ) -> None:

        row = self.table.currentRow()

        key = self.table.item(
            row,
            0,
        )

        key = WildcardField(
            base_value=key.text(),
            wildcard_sets=self.wildcard_sets,
        )

        del self.values[key]

        TableWidget.delete_current_row(
            self=self,
        )
