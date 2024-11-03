from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

from .wildcard_input_field_group_box import WildcardInputFieldGroupBox
from .......core.extensions.input_fields import WildcardPathInputField


class WildcardPathInputFieldGroupBox(
    WildcardInputFieldGroupBox,
):

    input_field: WildcardPathInputField
    browse_button: QPushButton

    def __init__(
        self,
        input_field: WildcardPathInputField,
    ) -> None:

        WildcardInputFieldGroupBox.__init__(
            self=self,
            input_field=input_field,
        )

        self.browse_button = QPushButton(
            'Browse',
        )

        self.browse_button.clicked.connect(
            self.browse,
        )

        self.layout.addWidget(
            self.browse_button,
            0,
            1,
        )

    def browse(
        self,
    ) -> None:

        path, _ = QFileDialog.getOpenFileName(
            caption=self.input_field.file_dialog_caption,
            filter=self.input_field.file_dialog_filter,
        )

        if path:
            self.line_edit.setText(
                path,
            )
