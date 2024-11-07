from PySide6.QtWidgets import QWidget, QVBoxLayout

from ......view.main_window.main_widget.object_viewer.input_field_group_boxes import (
    StringInputFieldGroupBox,
)
from .......core.input_fields.string_input_field import StringInputField


class DescriptionWidget(
    QWidget,
):

    layout: QVBoxLayout
    group_box: StringInputFieldGroupBox

    def __init__(
        self,
        description_field: StringInputField,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent=parent,
        )

        self.layout = QVBoxLayout()

        self.setLayout(
            self.layout,
        )

        self.group_box = StringInputFieldGroupBox(
            input_field=description_field,
        )

        self.layout.addWidget(
            self.group_box,
        )

        self.layout.addStretch()
