from .wildcard_field_base import WildcardFieldBase
from . import WildcardSets


class WildcardField(
    WildcardFieldBase,
):
    """
    Wildcard-linked text field.
    """

    _base_value: str

    def __init__(
        self,
        base_value: str,
        wildcard_sets: WildcardSets | None = None,
    ):
        WildcardFieldBase.__init__(
            self=self,
            wildcard_sets=wildcard_sets,
        )

        self._base_value = base_value

    @property
    def base_value(
        self,
    ) -> str:
        """
        Base value, without wildcard replacement.
        """

        return self._base_value

    @base_value.setter
    def base_value(
        self,
        value: str,
    ) -> None:
        """
        Base value, without wildcard replacement.
        """

        self._base_value = value
