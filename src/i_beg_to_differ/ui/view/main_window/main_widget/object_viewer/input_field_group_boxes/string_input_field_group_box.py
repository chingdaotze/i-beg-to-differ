from PySide6.QtWidgets import QPlainTextEdit, QSizePolicy

from .input_field_group_box import InputFieldGroupBox
from .......core.extensions.input_fields import StringInputField


class StringInputFieldGroupBox(
    InputFieldGroupBox,
):

    input_field: StringInputField
    text_edit: QPlainTextEdit

    def __init__(
        self,
        input_field: StringInputField,
    ):

        InputFieldGroupBox.__init__(
            self=self,
            input_field=input_field,
        )

        self.text_edit = QPlainTextEdit()

        self.text_edit.setPlainText(
            self.input_field.value,
        )

        self.text_edit.textChanged.connect(
            self.text_changed,
        )

        self.layout.addWidget(
            self.text_edit,
        )

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

    def text_changed(
        self,
    ) -> None:

        self.input_field.value = self.text_edit.toPlainText()
