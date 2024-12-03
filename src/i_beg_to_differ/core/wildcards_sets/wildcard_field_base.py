from abc import (
    ABC,
    abstractmethod,
)

from ..base import Base
from . import WildcardSets


class WildcardFieldBase(
    Base,
    ABC,
):
    """
    Abstract Wildcard-linked text field.
    """

    wildcard_sets: WildcardSets | None
    """
    Wildcard sets, used to perform replacement.
    """

    def __init__(
        self,
        wildcard_sets: WildcardSets | None = None,
    ):
        Base.__init__(
            self=self,
        )

        self.wildcard_sets = wildcard_sets

    def __str__(
        self,
    ) -> str:

        if self.wildcard_sets is not None:
            return self.wildcard_sets.replace_wildcards(
                string=self.base_value,
            )

        else:
            return self.base_value

    def __hash__(
        self,
    ) -> int:

        return hash(
            self.base_value,
        )

    def __float__(
        self,
    ) -> float:

        return float(
            str(
                self,
            ),
        )

    def __int__(
        self,
    ) -> int:

        return int(
            str(
                self,
            ),
        )

    def __bool__(
        self,
    ) -> bool:

        return bool(
            str(
                self,
            ),
        )

    @property
    @abstractmethod
    def base_value(
        self,
    ) -> str:
        """
        Base value, without wildcard replacement.
        """

    @base_value.setter
    @abstractmethod
    def base_value(
        self,
        value: str,
    ) -> None:
        """
        Base value, without wildcard replacement.
        """
