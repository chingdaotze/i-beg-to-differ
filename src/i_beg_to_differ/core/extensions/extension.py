from abc import ABC
from typing import ClassVar

from ..base import Base


class Extension(
    Base,
    ABC,
):
    """
    Base class for an IB2D extension.
    """

    extension_name: ClassVar[str]
    """
    Human-readable name for this extension.
    """

    extension_id: ClassVar[str]
    """
    Unique identifier for this extension. Set when the extension is registered.
    """

    def __init__(
        self,
    ):
        Base.__init__(
            self=self,
        )

    def __str__(
        self,
    ) -> str:

        return self.extension_id
