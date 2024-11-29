from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from .......core.compare_sets.compare_set.compare import Compare
from ......view.main_window.main_widget.object_viewer.input_field_group_boxes import (
    WildcardInputFieldGroupBox,
)


class DataSourcesWidget(
    QWidget,
):

    layout: QVBoxLayout
    compare: Compare

    source_field_group_box: WildcardInputFieldGroupBox
    target_field_group_box: WildcardInputFieldGroupBox

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

        self.source_field_group_box = WildcardInputFieldGroupBox(
            input_field=self.compare.source_data_source_ref.data_source_name,
        )

        self.layout.addWidget(
            self.source_field_group_box,
        )

        self.target_field_group_box = WildcardInputFieldGroupBox(
            input_field=self.compare.target_data_source_ref.data_source_name,
        )

        self.layout.addWidget(
            self.target_field_group_box,
        )

        self.layout.addStretch()
