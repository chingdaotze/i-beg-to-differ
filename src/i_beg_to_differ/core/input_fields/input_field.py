from abc import (
    ABC,
)
from ..base import Base


class InputField(
    Base,
    ABC,
):
    """
    Abstract class that represents an input field.
    """

    title: str | None

    def __init__(
        self,
        title: str | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.title = title
