from PySide6.QtWidgets import (
    QLineEdit,
    QLabel,
)

from .input_field_group_box import InputFieldGroupBox
from .......core.extensions.input_fields import WildcardInputField


class WildcardInputFieldGroupBox(
    InputFieldGroupBox,
):

    input_field: WildcardInputField
    line_edit: QLineEdit
    preview: QLabel

    def __init__(
        self,
        input_field: WildcardInputField,
    ):

        InputFieldGroupBox.__init__(
            self=self,
            input_field=input_field,
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

        font = self.preview.font()
        font.setItalic(
            True,
        )

        self.preview.setFont(
            font,
        )

        self.line_edit.editingFinished.connect(
            self.editing_finished,
        )

        self.line_edit.textChanged.connect(
            self.text_changed,
        )

        self.layout.addWidget(
            self.line_edit,
            0,
            0,
        )

        self.layout.addWidget(
            self.preview,
            1,
            0,
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
