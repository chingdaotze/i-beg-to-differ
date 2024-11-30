from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QVBoxLayout,
    QPushButton,
    QHeaderView,
    QLabel,
)

from ........core.compare_sets.compare_set.compare import Compare
from ........core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairData,
)
from .......view.main_window.main_widget.object_viewer.input_field_group_boxes.wildcard_input_field_widget import (
    WildcardInputFieldWidget,
)


class FieldReferencePairDataWidget(
    QWidget,
):

    compare: Compare
    layout: QGridLayout
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

        self.table = QTableWidget(
            0,
            5,
            self,
        )

        self.table.setHorizontalHeaderLabels(
            [
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

        for dt_field in self.compare.dt_fields:
            self.append_row(
                dt_field=dt_field,
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

        self.auto_match_button = QPushButton(
            'Auto-Match Fields',
            self,
        )

        self.add_button.clicked.connect(
            self.add_row,
        )

        self.delete_button.clicked.connect(
            self.delete_current_row,
        )

        self.auto_match_button.clicked.connect(
            self.auto_match_rows,
        )

        button_layout.addWidget(
            self.add_button,
        )

        button_layout.addWidget(
            self.delete_button,
        )

        button_layout.addWidget(
            self.auto_match_button,
        )

        button_layout.addStretch()

        self.layout.addLayout(
            button_layout,
            0,
            1,
        )

    def append_row(
        self,
        dt_field: FieldReferencePairData,
    ) -> None:
        # Assemble row widgets
        row_widgets = [
            WildcardInputFieldWidget(
                input_field=dt_field.source_field_ref.field_name,
                frame=False,
            ),
            QLabel(
                str(
                    dt_field.source_field_ref.transforms,
                )
            ),
            WildcardInputFieldWidget(
                input_field=dt_field.target_field_ref.field_name,
                frame=False,
            ),
            QLabel(
                str(
                    dt_field.target_field_ref.transforms,
                )
            ),
            QLabel(
                str(
                    dt_field.compare_rule,
                )
            ),
        ]

        # Add row
        self.add_row()
        row = self.table.rowCount()

        for column, row_widget in enumerate(row_widgets):

            self.table.setCellWidget(
                row - 1,
                column,
                row_widget,
            )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:

        # TODO: Rebuild dt_fields from widgets

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

    def auto_match_rows(
        self,
    ) -> None:

        self.table.setRowCount(
            0,
        )

        self.compare.dt_fields = self.compare.auto_match_dt_fields

        for dt_field in self.compare.dt_fields:
            self.append_row(
                dt_field=dt_field,
            )
