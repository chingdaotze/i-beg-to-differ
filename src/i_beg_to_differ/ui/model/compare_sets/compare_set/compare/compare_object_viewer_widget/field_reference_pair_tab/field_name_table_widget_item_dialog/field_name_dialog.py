from PySide6.QtWidgets import QWidget

from ........widgets import (
    Dialog,
    WildcardInputWidgetPreview,
)
from .........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from .........core.data_sources.data_source import DataSource


class FieldNameDialog(
    Dialog,
):

    field_reference: FieldReference
    data_source: DataSource | None

    wildcard_input_widget: WildcardInputWidgetPreview

    MIN_WIDTH = 300
    MIN_HEIGHT = 65

    def __init__(
        self,
        field_reference: FieldReference,
        data_source: DataSource | None = None,
        parent: QWidget | None = None,
    ):

        Dialog.__init__(
            self,
            title='Select Field Name',
            parent=parent,
        )

        self.field_reference = field_reference
        self.data_source = data_source

        if self.data_source is not None:
            self.wildcard_input_widget = WildcardInputWidgetPreview(
                wildcard_field=self.field_reference.field_name,
                options=self.data_source.columns,
            )

        else:
            self.wildcard_input_widget = WildcardInputWidgetPreview(
                wildcard_field=self.field_reference.field_name,
            )

        self.layout.addWidget(
            self.wildcard_input_widget,
            0,
            0,
        )

        self.layout.setRowStretch(
            1,
            1,
        )
