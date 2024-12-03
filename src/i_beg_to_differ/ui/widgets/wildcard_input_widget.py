from typing import (
    Callable,
    List,
)

from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
)

from ...core.wildcards_sets.wildcard_field import WildcardField
from . import (
    TextWidget,
    StaticComboBox,
    DynamicComboBox,
    LineEdit,
)


class WildcardInputWidget(
    QWidget,
):
    """
    Wildcard input field widget. Creates a text input field that updates the base value of a WildCard field. Options
    can be provided:
        - As a static list.
        - As a dynamic list, where a function provides option values. The function is recalculated every time
          the dropdown is activated.

    If options are provided, they appear as ``QComboBox`` options.
    """

    wildcard_field: WildcardField
    layout: QGridLayout
    preview: QLabel
    input_widget: TextWidget | QWidget

    def __init__(
        self,
        wildcard_field: WildcardField,
        options: List[str] | Callable[[], List[str]] | None = None,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent,
        )

        # Create WildCard field
        self.wildcard_field = wildcard_field

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

        # Create input widget
        if isinstance(options, list):
            # Static list
            self.input_widget = StaticComboBox(
                value=self.wildcard_field.base_value,
                options=options,
            )

        elif callable(options):
            # Dynamic list
            self.input_widget = DynamicComboBox(
                value=self.wildcard_field.base_value,
                options=options,
            )

        else:
            # Line edit
            self.input_widget = LineEdit(
                value=self.wildcard_field.base_value,
            )

        self.input_widget.text_changed.connect(
            self.text_changed,
        )

        self.input_widget.set_text(
            value=self.wildcard_field.base_value,
        )

        # Set layout
        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
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
