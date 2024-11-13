from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QGroupBox,
    QTableWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt

from .......core.compare_sets.compare_set.compare import Compare
from .......core.compare_sets.compare_set.compare.field_pair import (
    FieldPairPrimaryKey,
    FieldPairData,
)


class FieldsWidget(
    QWidget,
):

    compare: Compare
    layout: QGridLayout
    group_box: QGroupBox
    table: QTableWidget

    def __init__(
        self,
        compare: Compare,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent=parent,
        )

        self.compare = compare

        self.layout = QGridLayout(
            self,
        )

        self.group_box = QGroupBox(
            self,
        )

        self.table = QTableWidget(
            0,
            6,
            self,
        )

        self.table.setHorizontalHeaderLabels(
            [
                'Primary Key',
                'Source',
                'Source Transforms',
                'Target',
                'Target Transforms',
                'Compare Rule',
            ]
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

        for field_pair in self.compare.fields:
            self.append_row(
                field_pair=field_pair,
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

    def append_row(
        self,
        field_pair: FieldPairPrimaryKey | FieldPairData,
    ) -> None:
        # Build primary key widgets
        primary_key_checkbox = QTableWidgetItem()
        compare_rule = QTableWidgetItem()

        if isinstance(field_pair, FieldPairPrimaryKey):
            primary_key_checkbox.setCheckState(
                Qt.CheckState.Checked,
            )

            compare_rule.setText(
                '',
            )

        else:
            primary_key_checkbox.setCheckState(
                Qt.CheckState.Unchecked,
            )

            compare_rule.setText(
                str(
                    field_pair.compare_rule,
                ),
            )

        # Assemble row widgets
        row_widgets = [
            primary_key_checkbox,
            QTableWidgetItem(
                str(
                    field_pair.source_field,
                )
            ),
            QTableWidgetItem(
                str(
                    field_pair.source_transforms,
                )
            ),
            QTableWidgetItem(
                str(
                    field_pair.target_field,
                )
            ),
            QTableWidgetItem(
                str(
                    field_pair.target_transforms,
                )
            ),
            compare_rule,
        ]

        # Add row
        self.add_row()
        row = self.table.rowCount()

        for column, row_widget in enumerate(row_widgets):

            self.table.setItem(
                row - 1,
                column,
                row_widget,
            )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:

        # TODO: Rebuild pk_fields and dt_fields from widgets

        item = self.table.item(
            row,
            0,
        )

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

        item = self.table.item(
            row,
            0,
        )

        # TODO: Check if this event triggers cell_changed. If not, add a generic method to reload objects from table.

        self.table.removeRow(
            row,
        )
