from PySide6.QtWidgets import (
    QFormLayout,
    QLineEdit,
)

from .......core.extensions.input_fields import StringInputField


class ObjectViewerStringInputField(
    QFormLayout,
):

    input_field: StringInputField
    line_edit: QLineEdit

    def __init__(
        self,
        input_field: StringInputField,
    ):

        QFormLayout.__init__(
            self,
        )

        self.input_field = input_field
        self.line_edit = QLineEdit()

        self.line_edit.setText(
            self.input_field.value,
        )

        self.line_edit.editingFinished.connect(
            self.editing_finished,
        )

        self.addRow(
            self.input_field.label,
            self.line_edit,
        )

    def editing_finished(
        self,
    ) -> None:

        self.input_field.value = self.line_edit.text()
