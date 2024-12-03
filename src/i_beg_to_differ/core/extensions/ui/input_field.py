from abc import (
    ABC,
    abstractmethod,
)

from PySide6.QtWidgets import QWidget


class InputField(
    ABC,
):
    """
    Abstract class that represents an input field.
    """

    @property
    @abstractmethod
    def layout_component(
        self,
    ) -> QWidget:
        """
        Abstract method that represents a portion of a layout.
        """
