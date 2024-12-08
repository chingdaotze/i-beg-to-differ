from PySide6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
    QSizePolicy,
)

from ...core.wildcards_sets.wildcard_field import WildcardField
from .widget import Widget


class DescriptionWidget(
    Widget,
):
    """
    Description text widget. Creates a markdown editor and viewer.
    """

    wildcard_field: WildcardField
    text_edit: QPlainTextEdit

    def __init__(
        self,
        wildcard_field: WildcardField,
        parent: QWidget | None = None,
    ):

        Widget.__init__(
            self,
            parent,
        )

        self.wildcard_field = wildcard_field

        # Text editor
        self.text_edit = QPlainTextEdit()

        self.text_edit.textChanged.connect(
            self.text_changed,
        )

        self.text_edit.setPlainText(
            self.wildcard_field.base_value,
        )

        # Layout
        self.layout.addWidget(
            self.text_edit,
            0,
            0,
        )

        self.layout.setRowStretch(
            1,
            2,
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Maximum,
        )

    def text_changed(
        self,
    ) -> None:
        """
        Abstract method triggered whenever text is changed. Override this method to update values.
        """

        self.wildcard_field.base_value = self.text_edit.toPlainText()
