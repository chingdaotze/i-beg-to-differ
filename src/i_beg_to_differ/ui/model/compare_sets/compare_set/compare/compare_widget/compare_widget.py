from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
)

from .......core.compare_sets.compare_set.compare import Compare
from .description_widget import DescriptionWidget
from .data_sources_widget import DataSourcesWidget


class CompareWidget(
    QTabWidget,
):

    description_widget: DescriptionWidget
    data_sources_widget: DataSourcesWidget

    def __init__(
        self,
        compare: Compare,
        parent: QWidget | None = None,
    ):

        QTabWidget.__init__(
            self,
            parent=parent,
        )

        self.description_widget = DescriptionWidget(
            description_field=compare.description,
        )

        self.addTab(
            self.description_widget,
            'Description',
        )

        self.data_sources_widget = DataSourcesWidget(
            data_source_pair=compare.data_source_pair,
        )

        self.addTab(
            self.data_sources_widget,
            'Data Sources',
        )
