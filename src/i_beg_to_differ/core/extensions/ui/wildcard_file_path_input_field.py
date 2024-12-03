from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
)

from .wildcard_input_field import WildcardInputField
from ...wildcards_sets import WildcardSets


class WildcardFilePathInputField(
    WildcardInputField,
):
    """
    Identical in behavior to ``WildcardInputField``, except provides a file browser interface to select a
    single file.
    """

    file_dialog_caption: str
    file_dialog_filter: str

    def __init__(
        self,
        path: str,
        file_dialog_caption: str,
        file_dialog_filter: str,
        wildcard_sets: WildcardSets | None = None,
        title: str | None = None,
    ):

        WildcardInputField.__init__(
            self=self,
            base_value=path,
            wildcard_sets=wildcard_sets,
            title=title,
        )

        browse_button = QPushButton(
            'Browse',
        )

        browse_button.clicked.connect(
            self.browse,
        )

        self.wildcard_input_widget.layout.addWidget(
            browse_button,
            0,
            1,
        )

        self.file_dialog_caption = file_dialog_caption
        self.file_dialog_filter = file_dialog_filter

    def browse(
        self,
    ) -> None:

        path, _ = QFileDialog.getOpenFileName(
            caption=self.file_dialog_caption,
            filter=self.file_dialog_filter,
        )

        if path:
            self.input_widget.set_text(
                value=path,
            )
