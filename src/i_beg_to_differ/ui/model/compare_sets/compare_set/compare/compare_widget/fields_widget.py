from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QVBoxLayout,
    QPushButton,
    QHeaderView,
    QLabel,
    QCheckBox,
)
from PySide6.QtCore import Qt

from .......core.compare_sets.compare_set.compare import Compare
from .......core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ......view.main_window.main_widget.object_viewer.input_field_group_boxes.wildcard_input_field_widget import (
    WildcardInputFieldWidget,
)


class FieldsWidget(
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

        for field_ref_pair in self.compare.fields:
            self.append_row(
                field_ref_pair=field_ref_pair,
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
        field_ref_pair: FieldReferencePairPrimaryKey | FieldReferencePairData,
    ) -> None:
        # Build primary key widgets
        primary_key_checkbox = QCheckBox()
        compare_rule = QLabel()

        if isinstance(field_ref_pair, FieldReferencePairPrimaryKey):
            primary_key_checkbox.setCheckState(
                Qt.CheckState.Checked,
            )

            compare_rule.setText(
                '',
            )

        elif isinstance(field_ref_pair, FieldReferencePairData):
            primary_key_checkbox.setCheckState(
                Qt.CheckState.Unchecked,
            )

            compare_rule.setText(
                str(
                    field_ref_pair.compare_rule,
                ),
            )

        else:
            raise TypeError(
                f'Unhandled type for field_ref_pair: {type(field_ref_pair).__name__}!',
            )

        # Assemble row widgets
        row_widgets = [
            primary_key_checkbox,
            WildcardInputFieldWidget(
                input_field=field_pair.source_field_ref.field_name,
                frame=False,
            ),
            QLabel(
                str(
                    field_pair.source_transforms,
                )
            ),
            WildcardInputFieldWidget(
                input_field=field_pair.target_field,
                frame=False,
            ),
            QLabel(
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
