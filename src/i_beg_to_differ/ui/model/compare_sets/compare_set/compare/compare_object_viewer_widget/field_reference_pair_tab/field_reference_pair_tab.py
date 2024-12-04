from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from .field_reference_pair_primary_key_widget import FieldReferencePairPrimaryKeyWidget
from .field_reference_pair_data_widget import FieldReferencePairDataWidget
from ........core.compare_sets.compare_set.compare import Compare
from .......widgets import GroupBox


class FieldReferencePairTab(
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

        primary_key_group_box = GroupBox(
            title='Primary Keys',
        )

        self.field_reference_pair_primary_key_widget = (
            FieldReferencePairPrimaryKeyWidget(
                compare=compare,
            )
        )

        primary_key_group_box.layout.addWidget(
            self.field_reference_pair_primary_key_widget,
            0,
            0,
        )

        self.layout.addWidget(
            primary_key_group_box,
            0,
            0,
        )

        data_field_group_box = GroupBox(
            title='Data Fields',
        )

        self.field_reference_pair_data_widget = FieldReferencePairDataWidget(
            compare=compare,
        )

        data_field_group_box.layout.addWidget(
            self.field_reference_pair_data_widget,
            0,
            0,
        )

        self.layout.addWidget(
            data_field_group_box,
            0,
            1,
        )
