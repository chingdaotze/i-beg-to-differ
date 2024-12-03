from typing import List

from PySide6.QtWidgets import QWidget

from .combo_box import ComboBox


class StaticComboBox(
    ComboBox,
):
    """
    QComboBox with a static list of inputs.
    """

    _options: List[str]

    def __init__(
        self,
        options: List[str],
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

        return self._options
