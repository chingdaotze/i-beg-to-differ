from PySide6.QtWidgets import QWidget

from ....widgets import DescriptionWidget
from .....core.compare_sets.compare_set import CompareSet


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
            value=compare_set.description,
            parent=parent,
        )

    def text_changed(
        self,
    ) -> None:

        self.compare_set.description = self.text_edit.toPlainText()
