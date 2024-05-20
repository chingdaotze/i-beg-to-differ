from . import Wildcards


class WildcardField:
    """
    Wildcard-linked text field.
    """

    _base_value: str
    wildcards: Wildcards | None

    def __init__(
        self,
        base_value: str,
        wildcards: Wildcards | None = None,
    ):

        self._base_value = base_value
        self.wildcards = wildcards

    @property
    def base_value(
        self,
    ) -> str:
        """
        Base value without wildcard replacement.

        :return:
        """

        return self._base_value

    @property
    def value(
        self,
    ) -> str:
        """
        Base value with wildcard replacement.

        :return:
        """

        if self.wildcards is not None:
            return self.wildcards.replace_wildcards(
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
