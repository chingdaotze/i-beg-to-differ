from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from .field_reference_pair_primary_key_widget import FieldReferencePairPrimaryKeyWidget
from .field_reference_pair_data_widget import FieldReferencePairDataWidget
from ........core.compare_sets.compare_set.compare import Compare


class FieldReferencePairWidget(
    QWidget,
):

    field_reference_pair_primary_key_widget: FieldReferencePairPrimaryKeyWidget
    field_reference_pair_data_widget: FieldReferencePairDataWidget

    layout: QGridLayout

    def __init__(
        self,
        compare: Compare,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent=parent,
        )

        self.layout = QGridLayout()

        self.setLayout(
            self.layout,
        )

        self.field_reference_pair_primary_key_widget = (
            FieldReferencePairPrimaryKeyWidget(
                compare=compare,
            )
        )

        self.layout.addWidget(
            self.field_reference_pair_primary_key_widget,
            0,
            0,
        )

        self.field_reference_pair_data_widget = FieldReferencePairDataWidget(
            compare=compare,
        )

        self.layout.addWidget(
            self.field_reference_pair_data_widget,
            0,
            1,
        )
