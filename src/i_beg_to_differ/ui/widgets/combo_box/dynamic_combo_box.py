from typing import (
    Callable,
    List,
)

from PySide6.QtWidgets import QWidget

from .combo_box import ComboBox


class DynamicComboBox(
    ComboBox,
):
    """
    QComboBox with a dynamic list of inputs, recalculated whenever the dropdown appears.
    """

    _options: Callable[[], List[str]]

    def __init__(
        self,
        options: Callable[[], List[str]],
        value: str | None = None,
        parent: QWidget | None = None,
    ):

        ComboBox.__init__(
            self=self,
            value=value,
            parent=parent,
        )

        self._options = options

    @property
    def options(
        self,
    ) -> List[str]:

        return self._options()
