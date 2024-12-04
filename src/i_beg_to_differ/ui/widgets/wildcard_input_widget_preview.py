from typing import (
    Callable,
    List,
)

from PySide6.QtWidgets import (
    QLabel,
    QWidget,
)

from ...core.wildcards_sets.wildcard_field import WildcardField
from . import WildcardInputWidget


class WildcardInputWidgetPreview(
    WildcardInputWidget,
):
    """
    Wildcard input field widget. Creates a text input field that updates the base value of a WildCard field. Options
    can be provided:
        - As a static list.
        - As a dynamic list, where a function provides option values. The function is recalculated every time
          the dropdown is activated.

    If options are provided, they appear as ``QComboBox`` options.
    """

    preview: QLabel

    def __init__(
        self,
        wildcard_field: WildcardField,
        options: List[str] | Callable[[], List[str]] | None = None,
        parent: QWidget | None = None,
    ):

        WildcardInputWidget.__init__(
            self=self,
            wildcard_field=wildcard_field,
            options=options,
            parent=parent,
        )

        # Create preview
        self.preview = QLabel()

        font = self.preview.font()
        font.setItalic(
            True,
        )
        self.preview.setFont(
            font,
        )

        self.update_preview()

        self.layout.addWidget(
            self.preview,
            1,
            0,
        )

    def update_preview(
        self,
    ) -> None:

        self.preview.setText(
            str(
                self.wildcard_field,
            ),
        )

    def text_changed(
        self,
    ) -> None:

        self.wildcard_field.base_value = self.input_widget.get_text()
        self.update_preview()
