from typing import (
    Dict,
    Any,
)

from PySide6.QtWidgets import (
    QTableWidget,
    QWidget,
    QTableWidgetItem,
)

# FIXME: This class still isn't behaving right


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

        self.setColumnCount(
            2,
        )

        self.setRowCount(
            len(self.values) + 1,
        )

        self.key_column = key_column
        self.value_column = value_column

        self.setHorizontalHeaderLabels(
            [
                self.key_column,
                self.value_column,
            ]
        )

        self.verticalHeader().setVisible(
            False,
        )

        for key, value in self.values.items():
            self.append_row(
                key=key,
                value=value,
            )

        self.cellChanged.connect(
            self.cell_changed,
        )

    def append_row(
        self,
        key: Any,
        value: Any,
    ) -> None:
        # Calculate new row
        row = self.rowCount() + 1

        key_widget = QTableWidgetItem(
            key,
        )

        value_widget = QTableWidgetItem(
            value,
        )

        self.setItem(
            row,
            0,
            key_widget,
        )

        self.setItem(
            row,
            1,
            value_widget,
        )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:

        self.values.clear()

        for row in range(self.rowCount()):

            key = self.itemAt(
                row,
                0,
            ).text()

            value = self.itemAt(
                row,
                1,
            ).text()

            self.values[key] = value
