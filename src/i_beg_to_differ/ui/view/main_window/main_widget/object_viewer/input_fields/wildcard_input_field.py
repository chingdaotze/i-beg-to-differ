from PySide6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QLabel,
)

from .......core.extensions.input_fields import WildcardInputField


class ObjectViewerWildcardInputField(
    QFormLayout,
):

    input_field: WildcardInputField
    line_edit: QLineEdit
    preview: QLabel

    def __init__(
        self,
        input_field: WildcardInputField,
    ):

        QFormLayout.__init__(
            self,
        )

        self.input_field = input_field
        self.line_edit = QLineEdit()
        self.preview = QLabel()

        self.line_edit.setText(
            self.input_field.base_value,
        )

        self.preview.setText(
            str(self.input_field),
        )

        self.line_edit.editingFinished.connect(
            self.editing_finished,
        )

        self.line_edit.textChanged.connect(
            self.text_changed,
        )

        self.addRow(
            self.input_field.label,
            self.line_edit,
        )

        self.addRow(
            'Preview: ',
            self.preview,
        )

    def editing_finished(
        self,
    ) -> None:

        self.input_field.base_value = self.line_edit.text()

    def text_changed(
        self,
    ) -> None:

        self.input_field.base_value = self.line_edit.text()

        self.preview.setText(
            str(self.input_field),
        )
