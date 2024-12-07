from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
)
from PySide6.QtCore import QModelIndex

from .......widgets import (
    TableWidget,
    TableWidgetItemDialog,
)
from ........core.compare_sets.compare_set.compare import Compare
from ........core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairData,
)
from .field_name_table_widget_item import FieldNameTableWidgetItem
from .field_transform_table_widget_item import FieldTransformTableWidgetItem
from .compare_rule_table_widget_item import CompareRuleTableWidgetItem


class FieldReferencePairDataWidget(
    TableWidget,
):

    compare: Compare
    working_dir_path: Path

    def __init__(
        self,
        compare: Compare,
        working_dir_path: Path,
        parent: QWidget | None = None,
    ):

        TableWidget.__init__(
            self,
            columns=[
                'Source',
                'Source Transforms',
                'Target',
                'Target Transforms',
                'Compare Rule',
            ],
            parent=parent,
        )

        self.compare = compare
        self.working_dir_path = working_dir_path

        self.table.doubleClicked.connect(
            self.open_dialog,
        )

        for dt_field in self.compare.dt_fields:
            self.insert_table_widgets(
                dt_field=dt_field,
            )

        # Construct buttons
        self.auto_match_button = QPushButton(
            'Auto-Match Fields',
            self,
        )

        self.auto_match_button.clicked.connect(
            self.auto_match_rows,
        )

        self.button_layout.insertWidget(
            2,
            self.auto_match_button,
        )

    def add_row(
        self,
    ) -> None:

        # Add new data field pair
        dt_fields = self.compare.dt_fields

        dt_field = FieldReferencePairData(
            source_field_name='',
            target_field_name='',
            wildcard_sets=self.compare.wildcard_sets,
        )

        dt_fields.append(
            dt_field,
        )

        self.compare.dt_fields = dt_fields

        self.insert_table_widgets(
            dt_field=dt_field,
        )

    def delete_current_row(
        self,
    ) -> None:

        row = self.table.currentRow()

        dt_fields = self.compare.dt_fields
        del dt_fields[row]
        self.compare.dt_fields = dt_fields

        self.table.removeRow(
            row,
        )

    def insert_table_widgets(
        self,
        dt_field: FieldReferencePairData,
    ) -> None:

        # Assemble row items
        items = [
            FieldNameTableWidgetItem(
                field_reference=dt_field.source_field_ref,
                data_source=self.compare.source_data_source,
            ),
            FieldTransformTableWidgetItem(
                field_reference=dt_field.source_field_ref,
                working_dir_path=self.working_dir_path,
            ),
            FieldNameTableWidgetItem(
                field_reference=dt_field.target_field_ref,
                data_source=self.compare.target_data_source,
            ),
            FieldTransformTableWidgetItem(
                field_reference=dt_field.target_field_ref,
                working_dir_path=self.working_dir_path,
            ),
            CompareRuleTableWidgetItem(
                field_reference_pair=dt_field,
                working_dir_path=self.working_dir_path,
            ),
        ]

        # Add row
        row = self.table.rowCount()

        self.table.insertRow(
            row,
        )

        for column, item in enumerate(items):

            self.table.setItem(
                row,
                column,
                item,
            )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:

        item: TableWidgetItemDialog = self.table.item(
            row,
            column,
        )

        item.set_text()

    def auto_match_rows(
        self,
    ) -> None:

        self.table.setRowCount(
            0,
        )

        self.compare.dt_fields = self.compare.auto_match_dt_fields

        for dt_field in self.compare.dt_fields:
            self.insert_table_widgets(
                dt_field=dt_field,
            )

    def open_dialog(
        self,
        index: QModelIndex,
    ) -> None:

        item: TableWidgetItemDialog = self.table.itemFromIndex(
            index,
        )

        item.open_dialog()

        self.table.cellChanged.emit(
            index.row(),
            index.column(),
        )
