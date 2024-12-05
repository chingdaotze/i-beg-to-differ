from typing import (
    List,
    Tuple,
)

from PySide6.QtWidgets import QWidget, QComboBox

from .........widgets import Dialog
from ..........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from ..........core.data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)


class FieldTransformSelectorDialog(
    Dialog,
):

    field_reference: FieldReference
    field_transform_selector_widget: QComboBox
    extension_name_map: List[Tuple[str, FieldTransform]]

    def __init__(
        self,
        field_reference: FieldReference,
        parent: QWidget | None = None,
    ):

        Dialog.__init__(
            self=self,
            title='Select Field Transform',
            parent=parent,
        )

        self.field_reference = field_reference

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
        field_transform = self.extension_name_map[current_index][1]

        return field_transform
