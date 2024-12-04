from PySide6.QtWidgets import QWidget

from ......widgets import DescriptionWidget
from .......core.compare_sets.compare_set.compare import Compare


class CompareDescriptionTab(
    DescriptionWidget,
):

    compare: Compare

    def __init__(
        self,
        compare: Compare,
        parent: QWidget | None = None,
    ):

        self.compare = compare

        DescriptionWidget.__init__(
            self=self,
            value=compare.description,
            parent=parent,
        )

    def text_changed(
        self,
    ) -> None:

        self.compare.description = self.text_edit.toPlainText()
