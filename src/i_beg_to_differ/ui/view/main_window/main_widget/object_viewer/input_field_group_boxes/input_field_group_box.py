from PySide6.QtWidgets import (
    QGroupBox,
    QGridLayout,
)

from .......core.input_fields import InputField


class InputFieldGroupBox(
    QGroupBox,
):

    input_field: InputField
    layout: QGridLayout

    def __init__(
        self,
        input_field: InputField,
    ):

        QGroupBox.__init__(
            self,
        )

        self.input_field = input_field

        if self.input_field.title is not None:
            self.setTitle(
                self.input_field.title,
            )

        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )
