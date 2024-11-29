from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
)

from .......core.compare_sets.compare_set.compare import Compare
from .description_widget import DescriptionWidget
from .data_sources_widget import DataSourcesWidget
from .fields_widget import FieldsWidget


class CompareWidget(
    QTabWidget,
):

    description_widget: DescriptionWidget
    data_sources_widget: DataSourcesWidget
    fields_widget: FieldsWidget

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
            compare=compare,
        )

        self.addTab(
            self.data_sources_widget,
            'Data Sources',
        )

        self.fields_widget = FieldsWidget(
            compare=compare,
        )

        self.addTab(
            self.fields_widget,
            'Field Pairs',
        )
