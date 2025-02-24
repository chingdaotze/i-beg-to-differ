"""
Contains definition of the FieldNameTableWidgetItem class.
"""

from i_beg_to_differ.core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from i_beg_to_differ.core.data_sources.data_source import DataSource
from ........widgets import TableWidgetItemDialog
from .field_name_table_widget_item_dialog import FieldNameTableWidgetItemDialog


class FieldNameTableWidgetItem(
    TableWidgetItemDialog,
):
    """
    Table item that represents a Field Name.
    """

    field_reference: FieldReference
    data_source: DataSource | None

    def __init__(
        self,
        field_reference: FieldReference,
        data_source: DataSource | None = None,
    ):

        self.field_reference = field_reference
        self.data_source = data_source

        TableWidgetItemDialog.__init__(
            self=self,
        )

    def get_text(
        self,
    ) -> str:

        if self.field_reference is None:
            return ''

        return self.field_reference.field_name.base_value

    def open_dialog(
        self,
    ) -> None:

        dialog = FieldNameTableWidgetItemDialog(
            field_reference=self.field_reference,
            data_source=self.data_source,
        )

        dialog.exec()
