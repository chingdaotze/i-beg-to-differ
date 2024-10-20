from abc import ABC
from typing import ClassVar

from ...base import Base


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

    def __init__(
        self,
    ):
        Base.__init__(
            self=self,
        )

    def __str__(
        self,
    ) -> str:

        return self.get_extension_id()

    @classmethod
    def get_extension_id(
        cls,
    ) -> str:
        """
        Gets a unique identifier for this extension, based on the module name.

        :return:
        """

        # FIXME: This is actually a class property, but Python 3.13+ deprecates class properties.

        return cls.__module__.split('.')[-1]
