from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex

from .........widgets import TableWidget
from ..........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from ..........core.data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from .field_transform_selector_dialog import FieldTransformSelectorDialog
from .field_transform_list_table_widget_item import FieldTransformListTableWidgetItem


class FieldTransformListWidget(
    TableWidget,
):

    field_reference: FieldReference

    def __init__(
        self,
        field_reference: FieldReference,
        parent: QWidget | None = None,
    ):

        TableWidget.__init__(
            self=self,
            columns=[
                'Field Transforms',
            ],
            parent=parent,
        )

        self.field_reference = field_reference

        self.table.doubleClicked.connect(
            self.open_dialog,
        )

        for field_transform in self.field_reference.transforms:
            self.insert_table_widget(
                field_transform=field_transform,
            )

    def add_row(
        self,
    ) -> None:
        # TODO: Open a dialog to add transform. Transform dialog should open transform configuration dialog.

        field_transform_selector_dialog = FieldTransformSelectorDialog(
            field_reference=self.field_reference,
            parent=self,
        )

        field_transform_selector_dialog.exec()

        field_transform = field_transform_selector_dialog.field_transform

        self.field_reference.transforms.append(
            transform=field_transform,
        )

        self.insert_table_widget(
            field_transform=field_transform,
        )

    def cell_changed(
        self,
        row: int,
        column: int,
    ) -> None:
        item: FieldTransformListTableWidgetItem = self.table.item(
            row,
            column,
        )

        item.set_text()

    def delete_current_row(
        self,
    ) -> None:
        row = self.table.currentRow()

        del self.field_reference.transforms.transforms[row]

        self.table.removeRow(
            row,
        )

    def insert_table_widget(
        self,
        field_transform: FieldTransform,
    ) -> None:
        # Assemble row items
        items = [
            FieldTransformListTableWidgetItem(
                field_transform=field_transform,
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
        item: FieldTransformListTableWidgetItem = self.table.itemFromIndex(
            index,
        )

        item.open_dialog()

        self.table.cellChanged.emit(
            index.row(),
            index.column(),
        )
