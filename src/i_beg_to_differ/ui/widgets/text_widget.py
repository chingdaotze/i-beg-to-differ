from abc import abstractmethod

from PySide6.QtCore import SignalInstance


class TextWidget:
    """
    Abstract class that contains generic interfaces for interacting with text.
    """

    def __init__(
        self,
        value: str | None,
    ):

        if value is not None:
            self.set_text(
                value=value,
            )

    @property
    @abstractmethod
    def text_changed(
        self,
    ) -> SignalInstance:
        """
        Abstract property to get the signal that indicates text has changed.
        """

    @abstractmethod
    def get_text(
        self,
    ) -> str:
        """
        Abstract method to get the text of this widget.
        """

    @abstractmethod
    def set_text(
        self,
        value: str,
    ) -> None:
        """
        Abstract method to set the text of this widget.
        """
