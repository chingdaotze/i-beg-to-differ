from typing import Dict

from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
)

from .....ui.widgets import TableWidget
from ....wildcards_sets.wildcard_dict import WildcardDict


class WildcardDictTableWidget(
    TableWidget,
):
    """
    Widget that creates a table of key-value pairs, with Wildcard value substitution in both
    keys and values.
    """

    wildcard_dict: WildcardDict

    def __init__(
        self,
        wildcard_dict: WildcardDict,
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

        self.wildcard_dict = wildcard_dict

        for key, value in self.wildcard_dict.values.items():
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

        # Read table
        key = self.table.item(
            row,
            0,
        ).text()

        value = self.table.item(
            row,
            2,
        ).text()

        # Update previews
        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                str(
                    self.wildcard_dict.to_wildcard_field(
                        base_value=key,
                    ),
                ),
            ),
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem(
                str(
                    self.wildcard_dict.to_wildcard_field(
                        base_value=value,
                    ),
                ),
            ),
        )

        # Update wildcard dict
        self.wildcard_dict[key] = value

    def delete_current_row(
        self,
    ) -> None:

        row = self.table.currentRow()

        key = self.table.item(
            row,
            0,
        ).text()

        del self.wildcard_dict[key]

        TableWidget.delete_current_row(
            self=self,
        )
