from PySide6.QtWidgets import (
    QComboBox,
    QCompleter,
)

from .wildcard_input_field_group_box_base import WildcardInputFieldGroupBoxBase
from .......core.extensions.input_fields import WildcardListInputField


class WildcardListInputFieldGroupBox(
    WildcardInputFieldGroupBoxBase,
):

    input_field: WildcardListInputField
    combo_box: QComboBox
    completer: QCompleter

    def __init__(
        self,
        input_field: WildcardListInputField,
    ) -> None:

        WildcardInputFieldGroupBoxBase.__init__(
            self=self,
            input_field=input_field,
        )

        self.combo_box = QComboBox()

        self.completer = QCompleter(
            self.input_field.options,
        )

        self.combo_box.setCompleter(
            self.completer,
        )

        self.combo_box.setCurrentText(
            self.input_field.base_value,
        )

        self.combo_box.currentTextChanged.connect(
            self.current_text_changed,
        )

        self.layout.addWidget(
            self.combo_box,
            0,
            0,
        )

        self.layout.addWidget(
            self.preview,
            1,
            0,
        )

    def current_text_changed(
        self,
    ) -> None:

        self.input_field.base_value = self.combo_box.currentText()
        self.update_preview()
