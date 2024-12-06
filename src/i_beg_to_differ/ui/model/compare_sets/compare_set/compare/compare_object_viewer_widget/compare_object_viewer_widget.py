from pathlib import Path

from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
)

from .......core.compare_sets.compare_set.compare import Compare
from .compare_description_tab import CompareDescriptionTab
from .data_sources_tab import DataSourcesTab
from .field_reference_pair_tab import FieldReferencePairTab


class CompareObjectViewerWidget(
    QTabWidget,
):

    description_tab: CompareDescriptionTab
    data_sources_tab: DataSourcesTab
    field_reference_pair_tab: FieldReferencePairTab

    def __init__(
        self,
        compare: Compare,
        working_dir_path: Path,
        parent: QWidget | None = None,
    ):

        QTabWidget.__init__(
            self,
            parent=parent,
        )

        self.description_tab = CompareDescriptionTab(
            compare=compare,
        )

        self.addTab(
            self.description_tab,
            'Description',
        )

        self.data_sources_tab = DataSourcesTab(
            compare=compare,
        )

        self.addTab(
            self.data_sources_tab,
            'Data Sources',
        )

        self.field_reference_pair_tab = FieldReferencePairTab(
            compare=compare,
            working_dir_path=working_dir_path,
        )

        self.addTab(
            self.field_reference_pair_tab,
            'Field Pairs',
        )
