from .........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from .........core.data_sources.data_source import DataSource
from ........widgets import TableWidgetItemDialog
from .........core.wildcards_sets import WildcardSets
from .field_name_dialog import FieldNameDialog


class FieldNameTableWidgetItemDialog(
    TableWidgetItemDialog,
):

    field_reference: FieldReference
    data_source: DataSource | None

    def __init__(
        self,
        field_reference: FieldReference | None = None,
        data_source: DataSource | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        if field_reference is None:
            field_reference = FieldReference(
                field_name='',
                wildcard_sets=wildcard_sets,
            )

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

        else:
            return self.field_reference.field_name.base_value

    def open_dialog(
        self,
    ) -> None:

        dialog = FieldNameDialog(
            field_reference=self.field_reference,
            data_source=self.data_source,
        )

        dialog.exec()
