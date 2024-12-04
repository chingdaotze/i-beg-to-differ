from PySide6.QtWidgets import (
    QDialog,
    QWidget,
)

from ........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from .......widgets import TableWidgetItemDialog


class FieldTransformDialog(
    QDialog,
):

    field_reference: FieldReference

    def __init__(
        self,
        field_reference: FieldReference,
        parent: QWidget | None = None,
    ):

        QDialog.__init__(
            self,
            parent,
        )

        self.field_reference = field_reference


class FieldTransformTableItemDialog(
    TableWidgetItemDialog,
):

    field_reference: FieldReference

    def __init__(
        self,
        field_reference: FieldReference,
    ):

        self.field_reference = field_reference

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

        dialog = FieldTransformDialog(
            field_reference=self.field_reference,
        )

        dialog.exec()
