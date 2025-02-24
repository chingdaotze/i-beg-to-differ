"""
Contains definition of the CompareSetDescriptionWidget class.
"""

from PySide6.QtWidgets import QWidget

from i_beg_to_differ.core.compare_sets.compare_set import CompareSet
from i_beg_to_differ.core.wildcards_sets.wildcard_field import WildcardField
from ....widgets import DescriptionWidget


class CompareSetDescriptionWidget(
    DescriptionWidget,
):
    """
    Description widget for a CompareSet.
    """

    compare_set: CompareSet

    def __init__(
        self,
        compare_set: CompareSet,
        parent: QWidget | None = None,
    ):
        self.compare_set = compare_set

        DescriptionWidget.__init__(
            self=self,
            wildcard_field=WildcardField(
                base_value=compare_set.description,
            ),
            parent=parent,
        )

    def text_changed(
        self,
    ) -> None:

        self.compare_set.description = self.text_edit.toPlainText()
