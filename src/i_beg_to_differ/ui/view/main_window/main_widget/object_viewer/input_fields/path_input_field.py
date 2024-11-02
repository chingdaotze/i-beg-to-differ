from .wildcard_input_field import ObjectViewerWildcardInputField
from .......core.extensions.input_fields import PathInputField

from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
)


class ObjectViewerPathInputField(
    ObjectViewerWildcardInputField,
):

    browse_button: QPushButton

    def __init__(
        self,
        input_field: PathInputField,
    ) -> None:

        ObjectViewerWildcardInputField.__init__(
            self=self,
            input_field=input_field,
        )

        self.browse_button = QPushButton(
            'Browse',
        )

        self.browse_button.clicked.connect(
            self.browse,
        )

        self.insertRow(
            1,
            '',
            self.browse_button,
        )

    def browse(
        self,
    ) -> None:

        path, _ = QFileDialog.getOpenFileName(
            caption='Open *.ib2d File',
            filter='ib2d Files (*.ib2d)',
        )

        if path:
            self.line_edit.setText(
                path,
            )
