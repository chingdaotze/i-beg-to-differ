from pathlib import Path

from PySide6.QtWidgets import QWidget

from ........widgets import Dialog
from .........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from .field_transform_list_widget import FieldTransformListWidget


class FieldTransformTableWidgetItemDialog(
    Dialog,
):

    field_reference: FieldReference
    field_transform_list_widget: FieldTransformListWidget

    MIN_WIDTH = 300
    # MIN_HEIGHT = 65

    def __init__(
        self,
        field_reference: FieldReference,
        working_dir_path: Path,
        parent: QWidget | None = None,
    ):

        Dialog.__init__(
            self,
            title='Edit Field Transforms',
            parent=parent,
        )

        self.field_reference = field_reference

        self.field_transform_list_widget = FieldTransformListWidget(
            field_reference=self.field_reference,
            working_dir_path=working_dir_path,
            parent=self,
        )

        self.layout.addWidget(
            self.field_transform_list_widget,
            0,
            0,
        )
