from typing import (
    Dict,
    Any,
)

from PySide6.QtWidgets import (
    QTableWidget,
    QWidget,
    QTableWidgetItem,
)


class DictTableWidget(
    QTableWidget,
):

    values: Dict[Any, Any]
    key_column: str
    value_column: str

    def __init__(
        self,
        values: Dict[Any, Any],
        key_column: str = 'Parameter',
        value_column: str = 'Value',
        parent: QWidget | None = None,
    ):

        QTableWidget.__init__(
            self,
            parent,
        )

        self.values = values
        self.key_column = key_column
        self.value_column = value_column

        self.setHorizontalHeaderLabels(
            [
                self.key_column,
                self.value_column,
            ]
        )

        for key, value in self.values.items():
            self.append_row(
                key=key,
                value=value,
            )

    def append_row(
        self,
        key: Any,
        value: Any,
    ) -> None:
        # Calculate new row
        new_row_index = self.rowCount() + 1
