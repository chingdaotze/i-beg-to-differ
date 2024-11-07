from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
)

from .......core.compare_sets.compare_set.compare import Compare
from .description_widget import DescriptionWidget


class CompareWidget(
    QTabWidget,
):

    description_widget: DescriptionWidget

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
