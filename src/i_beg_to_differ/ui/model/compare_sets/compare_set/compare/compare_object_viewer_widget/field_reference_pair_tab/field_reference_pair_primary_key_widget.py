from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex

from .......widgets import (
    TableWidget,
    TableWidgetItemDialog,
)
from ........core.compare_sets.compare_set.compare import Compare
from ........core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairPrimaryKey,
)
from .field_name_table_widget_item import FieldNameTableWidgetItem
from .field_transform_table_widget_item import FieldTransformTableWidgetItem


class FieldReferencePairPrimaryKeyWidget(
    TableWidget,
):

    compare: Compare

    def __init__(
        self,
        compare: Compare,
        parent: QWidget | None = None,
    ):

        TableWidget.__init__(
            self,
            columns=[
                'Source',
                'Source Transforms',
                'Target',
                'Target Transforms',
            ],
            parent=parent,
        )

        self.compare = compare

        self.table.doubleClicked.connect(
            self.open_dialog,
        )

        for pk_field in self.compare.pk_fields:
            self.insert_table_widget(
                pk_field=pk_field,
            )

    def add_row(
        self,
    ) -> None:

        # Add new primary key field pair
        pk_fields = self.compare.pk_fields

        pk_field = FieldReferencePairPrimaryKey(
            source_field_name='',
            target_field_name='',
            wildcard_sets=self.compare.wildcard_sets,
        )

        pk_fields.append(
            pk_field,
        )

        self.compare.pk_fields = pk_fields

        self.insert_table_widget(
            pk_field=pk_field,
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

    def delete_current_row(
        self,
    ) -> None:

        row = self.table.currentRow()

        pk_fields = self.compare.pk_fields
        del pk_fields[row]
        self.compare.pk_fields = pk_fields

        self.table.removeRow(
            row,
        )

    def insert_table_widget(
        self,
        pk_field: FieldReferencePairPrimaryKey,
    ) -> None:

        # Assemble row items
        items = [
            FieldNameTableWidgetItem(
                field_reference=pk_field.source_field_ref,
                data_source=self.compare.source_data_source,
            ),
            FieldTransformTableWidgetItem(
                field_reference=pk_field.source_field_ref,
            ),
            FieldNameTableWidgetItem(
                field_reference=pk_field.target_field_ref,
                data_source=self.compare.target_data_source,
            ),
            FieldTransformTableWidgetItem(
                field_reference=pk_field.target_field_ref,
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
