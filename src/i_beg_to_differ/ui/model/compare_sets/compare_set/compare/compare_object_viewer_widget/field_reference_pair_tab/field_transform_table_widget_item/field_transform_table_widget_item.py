from pathlib import Path

from .........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from ........widgets import TableWidgetItemDialog
from .field_transform_table_widget_item_dialog import (
    FieldTransformTableWidgetItemDialog,
)


class FieldTransformTableWidgetItem(
    TableWidgetItemDialog,
):

    field_reference: FieldReference
    working_dir_path: Path

    def __init__(
        self,
        field_reference: FieldReference,
        working_dir_path: Path,
    ):

        self.field_reference = field_reference
        self.working_dir_path = working_dir_path

        TableWidgetItemDialog.__init__(
            self=self,
        )

    def get_text(
        self,
    ) -> str:

        return str(
            self.field_reference.transforms,
        )

    def open_dialog(
        self,
    ) -> None:

        dialog = FieldTransformTableWidgetItemDialog(
            field_reference=self.field_reference,
            working_dir_path=self.working_dir_path,
        )

        dialog.exec()
