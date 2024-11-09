from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ......view.main_window.main_widget.object_viewer.input_field_group_boxes import (
    WildcardInputFieldGroupBox,
)
from .......core.compare_sets.compare_set.compare.data_source_pair import DataSourcePair
from .......core.data_sources import DataSources


class DataSourcesWidget(
    QWidget,
):

    layout: QVBoxLayout

    source_field_group_box: WildcardInputFieldGroupBox
    target_field_group_box: WildcardInputFieldGroupBox

    def __init__(
        self,
        data_source_pair: DataSourcePair,
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

        self.source_field_group_box = WildcardInputFieldGroupBox(
            input_field=data_source_pair._source,
        )

        self.layout.addWidget(
            self.source_field_group_box,
        )

        self.target_field_group_box = WildcardInputFieldGroupBox(
            input_field=data_source_pair._target,
        )

        self.layout.addWidget(
            self.target_field_group_box,
        )

        self.layout.addStretch()
