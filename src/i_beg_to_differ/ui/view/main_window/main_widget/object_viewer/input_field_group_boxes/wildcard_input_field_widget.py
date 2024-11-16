from typing import Callable

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLineEdit,
)
from .dynamic_combo_box import DynamicComboBox
from .......core.input_fields.wildcard_input_fields import WildcardInputField
from .......core.input_fields.input_field_options import InputFieldOptions


class WildcardInputFieldWidget(
    QWidget,
):

    layout: QGridLayout
    input_field: WildcardInputField
    input_widget: QLineEdit | DynamicComboBox
    text_changed_callback: Callable | None

    def __init__(
        self,
        input_field: WildcardInputField,
        text_changed_callback: Callable | None = None,
        parent: QWidget | None = None,
        frame: bool = True,
    ):

        QWidget.__init__(
            self,
            parent=parent,
        )

        self.input_field = input_field
        self.text_changed_callback = text_changed_callback

        self.layout = QGridLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.setLayout(
            self.layout,
        )

        if isinstance(self.input_field.options, InputFieldOptions):
            self.input_widget = DynamicComboBox(
                input_field=self.input_field.options,
            )

            self.input_widget.setCurrentText(
                self.input_field.base_value,
            )

            self.input_widget.currentTextChanged.connect(
                self.text_changed_dynamic_combo_box,
            )

        else:
            self.input_widget = QLineEdit()

            self.input_widget.setText(
                self.input_field.base_value,
            )

            self.input_widget.textChanged.connect(
                self.text_changed_line_edit,
            )

        self.layout.addWidget(
            self.input_widget,
            0,
            0,
        )

        if not frame:
            self.input_widget.setFrame(
                False,
            )

    def text_changed_dynamic_combo_box(
        self,
    ) -> None:

        self.input_field.base_value = self.input_widget.currentText()

        if self.text_changed_callback is not None:
            self.text_changed_callback()

    def text_changed_line_edit(
        self,
    ) -> None:

        self.input_field.base_value = self.input_widget.text()

        if self.text_changed_callback is not None:
            self.text_changed_callback()
