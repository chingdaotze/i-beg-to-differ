from abc import ABC
from typing import ClassVar


class Extension(
    ABC,
):
    """
    Base class for an IB2D extension.
    """

    extension_id: ClassVar[str]
    """
    Unique identifier for this extension.
    """

    extension_name: ClassVar[str]
    """
    Human-readable name for this extension.
    """

    def __str__(
        self,
    ) -> str:

        return self.extension_id
