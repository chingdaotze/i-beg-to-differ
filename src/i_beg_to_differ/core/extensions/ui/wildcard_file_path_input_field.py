from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
    QWidget,
)

from .wildcard_input_field import WildcardInputField
from ...wildcards_sets import WildcardSets
from ....ui.widgets import (
    WildcardInputWidgetPreview,
    GroupBox,
)


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
            self.base_value = path

    @property
    def layout_component(
        self,
    ) -> QWidget:

        wildcard_input_widget = WildcardInputWidgetPreview(
            wildcard_field=self.wildcard_field,
            options=self.options,
        )

        browse_button = QPushButton(
            'Browse',
        )

        browse_button.clicked.connect(
            self.browse,
        )

        wildcard_input_widget.layout.addWidget(
            browse_button,
            0,
            1,
        )

        if self.title is not None:
            layout_component = GroupBox(
                title=self.title,
            )

            layout_component.layout.addWidget(
                wildcard_input_widget,
                0,
                0,
            )

        else:
            layout_component = wildcard_input_widget

        return layout_component
