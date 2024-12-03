from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from .......core.compare_sets.compare_set.compare import Compare
from ......widgets import (
    WildcardInputWidget,
    GroupBox,
)


class DataSourcesWidget(
    QWidget,
):

    layout: QVBoxLayout
    compare: Compare

    source_field_input_widget: WildcardInputWidget
    target_field_input_widget: WildcardInputWidget

    def __init__(
        self,
        compare: Compare,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent=parent,
        )

        self.compare = compare

        self.layout = QVBoxLayout()

        self.setLayout(
            self.layout,
        )

        source_field_group_box = GroupBox(
            title='Source',
        )

        self.source_field_input_widget = WildcardInputWidget(
            wildcard_field=self.compare.source_data_source_ref.data_source_name,
            options=self.compare.data_sources.list_data_sources,
        )

        source_field_group_box.layout.addWidget(
            self.source_field_input_widget,
            0,
            0,
        )

        self.layout.addWidget(
            source_field_group_box,
        )

        target_field_group_box = GroupBox(
            title='Target',
        )

        self.target_field_input_widget = WildcardInputWidget(
            wildcard_field=self.compare.target_data_source_ref.data_source_name,
            options=self.compare.data_sources.list_data_sources,
        )

        target_field_group_box.layout.addWidget(
            self.source_field_input_widget,
            0,
            0,
        )

        self.layout.addWidget(
            target_field_group_box,
        )

        self.layout.addStretch()
