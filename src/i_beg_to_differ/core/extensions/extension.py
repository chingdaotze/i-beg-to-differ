from abc import ABC


class Extension(
    ABC,
):
    """
    Base class for an IB2D extension.
    """

    extension_id: str
    """
    Unique identifier for this extension.
    """

    extension_name: str
    """
    Human-readable name for this extension.
    """

    def __init__(
        self,
        extension_id: str,
        extension_name: str,
    ):

        self.extension_id = extension_id
        self.extension_name = extension_name

    def __str__(
        self,
    ) -> str:

        return self.extension_id
