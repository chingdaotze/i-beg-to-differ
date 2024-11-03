from PySide6.QtWidgets import QLabel

from .input_field_group_box import InputFieldGroupBox
from .......core.extensions.input_fields import InputField


class WildcardInputFieldGroupBoxBase(
    InputFieldGroupBox,
):

    preview: QLabel

    def __init__(
        self,
        input_field: InputField,
    ):

        InputFieldGroupBox.__init__(
            self=self,
            input_field=input_field,
        )

        self.preview = QLabel()

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

    def update_preview(
        self,
    ) -> None:

        self.preview.setText(
            str(self.input_field),
        )
