from PySide6.QtWidgets import QWidget

from ....widgets import DescriptionWidget
from .....core.wildcards_sets.wildcard_set import WildcardSet


class WildcardSetDescriptionWidget(
    DescriptionWidget,
):

    wildcard_set: WildcardSet

    def __init__(
        self,
        wildcard_set: WildcardSet,
        parent: QWidget | None = None,
    ):
        self.wildcard_set = wildcard_set

        DescriptionWidget.__init__(
            self=self,
            value=wildcard_set.description,
            parent=parent,
        )

    def text_changed(
        self,
    ) -> None:

        self.wildcard_set.description = self.text_edit.toPlainText()
