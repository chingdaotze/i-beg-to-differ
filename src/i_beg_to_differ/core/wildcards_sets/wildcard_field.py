from ..base import (
    Base,
    log_exception,
)
from . import WildcardSets


class WildcardField(
    Base,
):
    """
    Wildcard-linked text field.
    """

    _base_value: str

    wildcard_sets: WildcardSets | None
    """
    Wildcard sets, used to perform replacement.
    """

    def __init__(
        self,
        base_value: str,
        wildcard_sets: WildcardSets | None = None,
    ):
        Base.__init__(
            self=self,
        )

        self._base_value = base_value
        self.wildcard_sets = wildcard_sets

    @property
    def base_value(
        self,
    ) -> str:
        """
        Base value, without wildcard replacement.

        :return: Base value.
        """

        return self._base_value

    @property
    @log_exception
    def value(
        self,
    ) -> str:
        """
        Base value, with wildcard replacement.

        :return: Replaced value.
        """

        if self.wildcard_sets is not None:
            return self.wildcard_sets.replace_wildcards(
                string=self.base_value,
            )

        else:
            return self.base_value

    def __repr__(
        self,
    ) -> str:

        return self.base_value

    def __str__(
        self,
    ):

        return self.value
