from PySide6.QtWidgets import QWidget

from ....widgets import DescriptionWidget
from .....core.compare_sets.compare_set import CompareSet
from .....core.wildcards_sets.wildcard_field import WildcardField


class CompareSetDescriptionWidget(
    DescriptionWidget,
):

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
