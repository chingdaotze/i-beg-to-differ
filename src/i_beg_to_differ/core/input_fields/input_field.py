from abc import (
    ABC,
)


class InputField(
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

        self.title = title
