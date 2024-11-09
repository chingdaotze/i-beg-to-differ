from PySide6.QtWidgets import (
    QComboBox,
    QCompleter,
    QWidget,
)
from ........core.input_fields.input_field_options import InputFieldOptions


class DynamicComboBox(
    QComboBox,
):

    input_field: InputFieldOptions

    def __init__(
        self,
        input_field: InputFieldOptions,
        parent: QWidget | None = None,
    ):

        QComboBox.__init__(
            self,
            parent,
        )

        self.input_field = input_field

        self.setEditable(
            True,
        )

        self.setInsertPolicy(
            QComboBox.InsertPolicy.NoInsert,
        )

    def showPopup(
        self,
    ) -> None:

        self.clear()

        options = self.input_field.options

        self.addItems(
            options,
        )

        self.setCompleter(
            QCompleter(
                options,
                self,
            ),
        )

        QComboBox.showPopup(
            self,
        )
