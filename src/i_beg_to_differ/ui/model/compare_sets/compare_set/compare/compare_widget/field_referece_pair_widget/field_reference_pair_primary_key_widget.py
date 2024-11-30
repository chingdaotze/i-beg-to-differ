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
    FieldReferencePairPrimaryKey,
)
from .......view.main_window.main_widget.object_viewer.input_field_group_boxes.wildcard_input_field_widget import (
    WildcardInputFieldWidget,
)


class FieldReferencePairPrimaryKeyWidget(
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
            4,
            self,
        )

        self.table.setHorizontalHeaderLabels(
            [
                'Source',
                'Source Transforms',
                'Target',
                'Target Transforms',
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

        for pk_field in self.compare.pk_fields:
            self.append_row(
                pk_field=pk_field,
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
        pk_field: FieldReferencePairPrimaryKey,
    ) -> None:
        # Assemble row widgets
        row_widgets = [
            WildcardInputFieldWidget(
                input_field=pk_field.source_field_ref.field_name,
                frame=False,
            ),
            QLabel(
                str(
                    pk_field.source_field_ref.transforms,
                )
            ),
            WildcardInputFieldWidget(
                input_field=pk_field.target_field_ref.field_name,
                frame=False,
            ),
            QLabel(
                str(
                    pk_field.target_field_ref.transforms,
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

        # TODO: Rebuild pk_fields from widgets

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
