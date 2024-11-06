from PySide6.QtWidgets import QLineEdit

from .wildcard_input_field_group_box_base import WildcardInputFieldGroupBoxBase
from .......core.input_fields.wildcard_input_fields import WildcardInputField


class WildcardInputFieldGroupBox(
    WildcardInputFieldGroupBoxBase,
):

    input_field: WildcardInputField
    line_edit: QLineEdit

    def __init__(
        self,
        input_field: WildcardInputField,
    ):

        WildcardInputFieldGroupBoxBase.__init__(
            self=self,
            input_field=input_field,
        )

        self.line_edit = QLineEdit()

        self.line_edit.setText(
            self.input_field.base_value,
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

    def text_changed(
        self,
    ) -> None:

        self.input_field.base_value = self.line_edit.text()
        self.update_preview()
