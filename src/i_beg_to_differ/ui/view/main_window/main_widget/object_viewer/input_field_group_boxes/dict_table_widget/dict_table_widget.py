from typing import (
    Dict,
    Any,
)
from multiprocessing.managers import DictProxy

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QPushButton,
    QVBoxLayout,
    QTableWidgetItem,
)


class DictTableWidget(
    QWidget,
):

    values: Dict[Any, Any] | DictProxy
    key_column: str
    value_column: str

    layout: QGridLayout
    table: QTableWidget
    add_button: QPushButton
    delete_button: QPushButton

    def __init__(
        self,
        values: Dict[Any, Any] | DictProxy,
        key_column: str = 'Parameter',
        value_column: str = 'Value',
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent,
        )

        self.values = values
        self.key_column = key_column
        self.value_column = value_column

        self.layout = QGridLayout()
        self.setLayout(
            self.layout,
        )

        # Construct table
        self.table = QTableWidget(
            0,
            2,
            self,
        )

        self.table.setHorizontalHeaderLabels(
            [
                self.key_column,
                self.value_column,
            ]
        )

        self.table.verticalHeader().setVisible(
            False,
        )

        self.table.setShowGrid(
            True,
        )

        for key, value in self.values.items():
            self.append_row(
                key=key,
                value=value,
            )

        self.table.cellChanged.connect(
            self.cell_changed,
        )

        self.layout.addWidget(
            self.table,
            0,
            0,
        )

        # Construct buttons
        button_layout = QVBoxLayout()

        self.add_button = QPushButton(
            'Add',
            self,
        )

        self.delete_button = QPushButton(
            'Delete',
            self,
        )

        self.add_button.clicked.connect(
            self.add_row,
        )

        self.delete_button.clicked.connect(
            self.delete_current_row,
        )

        button_layout.addWidget(
            self.add_button,
        )

        button_layout.addWidget(
            self.delete_button,
        )

        button_layout.addStretch()

        self.layout.addLayout(
            button_layout,
            0,
            1,
        )

    @staticmethod
    def key_to_str(
        key: Any,
    ) -> str:

        return key

    @staticmethod
    def str_to_key(
        key: str,
    ) -> Any:

        return key

    @staticmethod
    def value_to_str(
        value: Any,
    ) -> str:

        return value

    @staticmethod
    def str_to_value(
        value: str,
    ) -> Any:

        return value

    def append_row(
        self,
        key: Any,
        value: Any,
    ) -> None:
        # Calculate new row
        self.add_row()

        row = self.table.rowCount()

        key = self.key_to_str(
            key=key,
        )

        key_widget = QTableWidgetItem(
            key,
        )

        value = self.value_to_str(
            value=value,
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
            key = self.str_to_key(
                key=key.text(),
            )

        value = self.table.item(
            row,
            1,
        )

        if isinstance(value, QTableWidgetItem):
            value = self.str_to_value(
                value=value.text(),
            )

        self.values[key] = value

    def add_row(
        self,
    ) -> None:

        self.table.insertRow(
            self.table.rowCount(),
        )

    def delete_current_row(
        self,
    ) -> None:

        row = self.table.currentRow()

        key = self.table.item(
            row,
            0,
        )

        if isinstance(key, QTableWidgetItem):
            key = self.str_to_key(
                key=key.text(),
            )

            del self.values[key]

        self.table.removeRow(
            row,
        )
