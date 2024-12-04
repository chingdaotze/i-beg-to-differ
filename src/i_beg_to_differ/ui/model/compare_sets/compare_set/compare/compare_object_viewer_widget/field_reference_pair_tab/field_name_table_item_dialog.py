from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QWidget,
)

from ........core.compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from ........core.data_sources.data_source import DataSource
from .......widgets import (
    WildcardInputWidgetPreview,
    TableItemDialog,
)
from ........core.wildcards_sets import WildcardSets


class FieldNameDialog(
    QDialog,
):

    field_reference: FieldReference
    data_source: DataSource | None

    layout: QGridLayout
    wildcard_input_widget: WildcardInputWidgetPreview

    MIN_WIDTH: int = 300
    MIN_HEIGHT: int = 100

    def __init__(
        self,
        field_reference: FieldReference,
        data_source: DataSource | None = None,
        parent: QWidget | None = None,
    ):

        QDialog.__init__(
            self,
            parent,
        )

        self.field_reference = field_reference
        self.data_source = data_source

        self.setWindowTitle(
            'Select Field Name',
        )

        self.resize(
            self.MIN_WIDTH,
            self.MIN_HEIGHT,
        )

        self.setMinimumWidth(
            self.MIN_WIDTH,
        )

        self.setMinimumHeight(
            self.MIN_HEIGHT,
        )

        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )

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


class FieldNameTableItemDialog(
    TableItemDialog,
):

    field_reference: FieldReference
    data_source: DataSource | None

    def __init__(
        self,
        field_reference: FieldReference | None = None,
        data_source: DataSource | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        if field_reference is None:
            field_reference = FieldReference(
                field_name='',
                wildcard_sets=wildcard_sets,
            )

        self.field_reference = field_reference
        self.data_source = data_source

        TableItemDialog.__init__(
            self=self,
        )

    def get_text(
        self,
    ) -> str:

        if self.field_reference is None:
            return ''

        else:
            return self.field_reference.field_name.base_value

    def open_dialog(
        self,
    ) -> None:

        dialog = FieldNameDialog(
            field_reference=self.field_reference,
            data_source=self.data_source,
        )

        dialog.exec()
