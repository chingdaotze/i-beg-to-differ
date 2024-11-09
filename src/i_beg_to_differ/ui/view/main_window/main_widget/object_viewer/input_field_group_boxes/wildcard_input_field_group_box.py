from PySide6.QtWidgets import QLineEdit

from .dynamic_combo_box import DynamicComboBox
from .wildcard_input_field_group_box_base import WildcardInputFieldGroupBoxBase
from .......core.input_fields.wildcard_input_fields import WildcardInputField
from .......core.input_fields.input_field_options import InputFieldOptions


class WildcardInputFieldGroupBox(
    WildcardInputFieldGroupBoxBase,
):

    input_field: WildcardInputField
    input_widget: QLineEdit | DynamicComboBox

    def __init__(
        self,
        input_field: WildcardInputField,
    ):

        WildcardInputFieldGroupBoxBase.__init__(
            self=self,
            input_field=input_field,
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

        self.layout.addWidget(
            self.preview,
            1,
            0,
        )

    def text_changed_dynamic_combo_box(
        self,
    ) -> None:

        self.input_field.base_value = self.input_widget.currentText()
        self.update_preview()

    def text_changed_line_edit(
        self,
    ) -> None:

        self.input_field.base_value = self.input_widget.text()
        self.update_preview()
