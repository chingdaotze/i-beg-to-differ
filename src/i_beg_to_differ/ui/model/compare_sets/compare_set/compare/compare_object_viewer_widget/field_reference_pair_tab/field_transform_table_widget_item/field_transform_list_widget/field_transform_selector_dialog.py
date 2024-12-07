from pathlib import Path
from typing import (
    List,
    Tuple,
    Type,
)

from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
)

from .........widgets import Dialog
from ..........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from ..........core.data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from ..........core.extensions.extension.custom_python_extension import (
    CustomPythonExtension,
)


class FieldTransformSelectorDialog(
    Dialog,
):

    field_reference: FieldReference
    working_dir_path: Path
    field_transform_selector_widget: QComboBox
    extension_name_map: List[Tuple[str, Type[FieldTransform]]]

    def __init__(
        self,
        field_reference: FieldReference,
        working_dir_path: Path,
        parent: QWidget | None = None,
    ):

        Dialog.__init__(
            self=self,
            title='Select Field Transform',
            parent=parent,
        )

        self.field_reference = field_reference
        self.working_dir_path = working_dir_path

        self.extension_name_map = [
            (field_transform.extension_name, field_transform)
            for field_transform in self.field_reference.transforms.transform_extensions.collection.values()
        ]

        self.field_transform_selector_widget = QComboBox(
            self,
        )

        self.field_transform_selector_widget.addItems(
            [
                extension_name_mapping[0]
                for extension_name_mapping in self.extension_name_map
            ],
        )

        self.layout.addWidget(
            self.field_transform_selector_widget,
            0,
            0,
        )

    @property
    def field_transform(
        self,
    ) -> FieldTransform:

        current_index = self.field_transform_selector_widget.currentIndex()
        field_transform_type = self.extension_name_map[current_index][1]

        # FIXME: Some classes require wildcard_sets. Figure out how to pass those in.

        if issubclass(field_transform_type, CustomPythonExtension):
            field_transform = field_transform_type(
                working_dir_path=self.working_dir_path,
            )

        else:
            field_transform = field_transform_type()

        return field_transform
