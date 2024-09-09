from ..base import Base
from . import WildcardSets


class WildcardField(
    Base,
):
    """
    Wildcard-linked text field.
    """

    base_value: str
    """
    Base value, without wildcard replacement.
    """

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

        self.base_value = base_value
        self.wildcard_sets = wildcard_sets

    def __str__(
        self,
    ):

        if self.wildcard_sets is not None:
            return self.wildcard_sets.replace_wildcards(
                string=self.base_value,
            )

        else:
            return self.base_value
