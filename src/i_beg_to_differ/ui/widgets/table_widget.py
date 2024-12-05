from typing import List
from abc import abstractmethod

from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QPushButton,
    QHeaderView,
    QVBoxLayout,
)

from .widget import Widget


class TableWidget(
    Widget,
):

    columns: List[str]
    table: QTableWidget
    add_button: QPushButton
    delete_button: QPushButton

    def __init__(
        self,
        columns: List[str],
        parent: QWidget | None = None,
    ):

        Widget.__init__(
            self,
            parent,
        )

        self.columns = columns

        # Construct table
        self.table = QTableWidget(
            0,
            len(self.columns),
            self,
        )

        self.table.setHorizontalHeaderLabels(
            columns,
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self.table.verticalHeader().setVisible(
            False,
        )

        self.table.setShowGrid(
            True,
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

    @abstractmethod
    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:
        """
        Abstract method that is called whenever a cell changes.
        """

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

        self.table.removeRow(
            row,
        )
