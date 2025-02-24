"""
Contains definition of the FieldReferencePairPrimaryKeyWidget class.
"""

from pathlib import Path

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex

from i_beg_to_differ.core.compare_sets.compare_set.compare import Compare
from i_beg_to_differ.core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairPrimaryKey,
)
from .......widgets import (
    TableWidget,
    TableWidgetItemDialog,
)
from .field_name_table_widget_item import FieldNameTableWidgetItem
from .field_transform_table_widget_item import FieldTransformTableWidgetItem


class FieldReferencePairPrimaryKeyWidget(
    TableWidget,
):
    """
    Widget that renders Field Reference Primary Key Pairs in a table.
    """

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
            ],
            parent=parent,
        )

        self.compare = compare
        self.working_dir_path = working_dir_path

        self.table.doubleClicked.connect(
            self.open_dialog,
        )

        for pk_field in self.compare.pk_fields:
            self.insert_table_widgets(
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

        self.insert_table_widgets(
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

    def insert_table_widgets(
        self,
        pk_field: FieldReferencePairPrimaryKey,
    ) -> None:
        """
        Inserts a Field Reference Primary Key Pair into the table.
        
        :param dt_field: Field Reference Primary Key Pair to insert.
        """

        # Assemble row items
        items = [
            FieldNameTableWidgetItem(
                field_reference=pk_field.source_field_ref,
                data_source=self.compare.source_data_source,
            ),
            FieldTransformTableWidgetItem(
                field_reference=pk_field.source_field_ref,
                working_dir_path=self.working_dir_path,
            ),
            FieldNameTableWidgetItem(
                field_reference=pk_field.target_field_ref,
                data_source=self.compare.target_data_source,
            ),
            FieldTransformTableWidgetItem(
                field_reference=pk_field.target_field_ref,
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

    def open_dialog(
        self,
        index: QModelIndex,
    ) -> None:
        """
        Opens a dialog provided by a `TableWidgetItemDialog` object.

        :param index: Index for the item to open.
        """

        item: TableWidgetItemDialog = self.table.itemFromIndex(
            index,
        )

        item.open_dialog()

        self.table.cellChanged.emit(
            index.row(),
            index.column(),
        )
